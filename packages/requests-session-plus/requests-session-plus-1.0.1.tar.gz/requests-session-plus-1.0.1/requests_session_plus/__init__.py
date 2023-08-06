"""requests_session_plus/__init__.py.

Drop in replacement for requests.Session() object that supports:
    - toggle on/off retries with helpful defaults
    - toggle on/off certificate checks and warnings
    - toggle on/off raising exception for client/server errors (status code >= 400)
    - sets global timeout for all HTTP calls
"""

import warnings
from typing import Any, Dict, List, Optional

from requests import Response, Session
from urllib3.exceptions import HTTPWarning
from urllib3.util.retry import Retry

__all__: List[str] = ["SessionPlus"]


RETRY_BACKOFF_FACTOR: float = 2
RETRY_STATUS_FORCELIST: List[int] = [
    413,  # Client: Payload Too Large
    429,  # Client: Too Many Requests
    500,  # Server: Internal Server Error
    502,  # Server: Bad Gateway
    503,  # Server: Service Unavailable
    504,  # Server: Gateway Timeout
]
RETRY_TOTAL: int = 5
TIMEOUT: float = 10


class SessionPlus(Session):
    """requests.Session() object with some quality of life enhancements."""

    _retry: bool
    _retry_backof_factor: float
    _retry_status_forcelist: List[int]
    _retry_total: int
    _status_exceptions: bool
    _timeout: Optional[float]
    _verify: bool

    def __init__(
        self,
        retry: bool = False,
        retry_backoff_factor: float = RETRY_BACKOFF_FACTOR,
        retry_status_forcelist: List[int] = RETRY_STATUS_FORCELIST,
        retry_total: int = RETRY_TOTAL,
        status_exceptions: bool = False,
        timeout: Optional[float] = TIMEOUT,
        verify: bool = True,
        **kwargs,
    ):
        """Instantiate SessionPlus object with timeout enabled.

        Args:
            retry (bool): enable/disable retries.  Defaults to False
            retry_backoff_factor (float): used when calculating time between retries.  Defaults to 2
            retry_status_forcelist (list[int]): status codes to issue retries for.  Defaults to [413,429,500,502-504]
            retry_total (int): total number of retries to attempt.  Defaults to 5
            status_exceptions (bool): raise exceptions for status codes >=400.  Defaults to False
            timeout (int or None): timeout for HTTP calls.  Defaults to 10
            verify (bool): enable/disable certificate verification.  Defaults to True

        """
        super().__init__()

        self.retry_backoff_factor = retry_backoff_factor
        self.retry_status_forcelist = retry_status_forcelist
        self.retry_total = retry_total

        # load any additional namespaced retry settings as attributes
        for key, value in kwargs.items():
            if key.startswith("retry_"):
                self.__dict__[key] = value

        self.retry = retry

        self.status_exceptions = status_exceptions

        self.timeout = timeout

        self.verify = verify

    @property
    def retry(self) -> bool:
        """Property to determine if retries are enabled/disabled."""
        return self._retry

    @retry.setter
    def retry(self, value: bool):
        """Set boolean value then call helper function to enable/disable retries."""
        self._retry = bool(value)
        self.update_retry()

    def update_retry(self):
        """Re-apply the Retry class with updated variables."""
        if self._retry:
            retry = Retry(**self.retry_settings)

        else:
            retry = Retry(total=0, read=False)

        for adapter in self.adapters.values():
            adapter.max_retries = retry

    @property
    def retry_backoff_factor(self) -> float:
        """Property used to determine backoff sleep time between retries."""
        return self._retry_backoff_factor

    @retry_backoff_factor.setter
    def retry_backoff_factor(self, value: float):
        """Validate the value is a float."""
        self._retry_backoff_factor = float(value)

    @property
    def retry_status_forcelist(self) -> List[int]:
        """Property used to determine which status codes require a retry."""
        return self._retry_status_forcelist

    @retry_status_forcelist.setter
    def retry_status_forcelist(self, values: List[int]):
        """Validate the value is a list of integers."""
        if not isinstance(values, list):
            raise ValueError("retry_status_forcelist must be a list of integers")

        new_list: List[int] = []

        for value in values:
            new_list.append(int(value))

        self._retry_status_forcelist = new_list

    @property
    def retry_total(self) -> int:
        """Property to return the total number of retries."""
        return self._retry_total

    @retry_total.setter
    def retry_total(self, value: int):
        """Validate the value is an integer."""
        self._retry_total = int(value)

    @property
    def retry_settings(self) -> Dict[str, Any]:
        """Property to generate the Retry settings dictionary."""
        settings: Dict[str, Any] = {
            "backoff_factor": self._retry_backoff_factor,
            "status_forcelist": self._retry_status_forcelist,
            "total": self._retry_total,
        }
        for key, value in self.__dict__.items():
            if key.startswith("retry_"):
                settings[key.replace("retry_", "")] = value

        return settings

    @property
    def status_exceptions(self) -> bool:
        """Property to determine if exceptions should be raised for status codes >=400."""
        return self._status_exceptions

    @status_exceptions.setter
    def status_exceptions(self, value: bool):
        """Set the value then modify the response hooks."""
        self._status_exceptions = bool(value)

        entry_index: Optional[int] = None

        for i, hook in enumerate(self.hooks["response"]):
            if hook.__name__ == self._status_exception_response_hook.__name__:
                entry_index = i
                break

        if self._status_exceptions and not isinstance(entry_index, int):
            self.hooks["response"].append(self._status_exception_response_hook)

        elif not self._status_exceptions and isinstance(entry_index, int):
            self.hooks["response"].pop(entry_index)

    def _status_exception_response_hook(self, response: Response, *args, **kwargs):
        """Set the post-response hook to raise an exception if HTTP status code is >=400.

        Args:
            response (Response): The object returned after HTTP call is made
        """
        response.raise_for_status()

    @property
    def timeout(self) -> Optional[float]:
        """Property to determine maximum time to wait for HTTP response before raising exception."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: Optional[float]):
        """Timeout can be number >0 or None where None disables timeout."""
        if isinstance(value, (float, int, str)):
            value = float(value)
            if value <= 0.0:
                raise ValueError("timeout must be a float or integer greater than 0")

        elif value is None:
            pass

        else:
            raise ValueError("timeout must be a float or integer greater than 0")

        self._timeout = value

    @property  # type: ignore
    def verify(self) -> bool:
        """Property to determine if certificates should be validated or not."""
        return self._verify

    @verify.setter
    def verify(self, value: bool):
        """Set the boolean them cycle through each warning and add/remove warnings as needed."""
        self._verify = bool(value)

        key: str = "default" if self._verify else "ignore"
        pop_filters: List[int] = []
        filter_found: bool = False

        for i, warn in enumerate(warnings.filters):
            if warn[2] == HTTPWarning:
                if warn[0] == key:
                    filter_found = True
                else:
                    pop_filters.append(i)

        if pop_filters:
            pop_filters.reverse()
            for filter_index in pop_filters:
                warnings.filters.pop(filter_index)  # type: ignore

        if not filter_found:
            warnings.simplefilter(key, HTTPWarning)  # type: ignore

    def send(self, request, **kwargs):
        """Send a given PreparedRequest."""
        if not kwargs.get("timeout") and self.timeout:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
