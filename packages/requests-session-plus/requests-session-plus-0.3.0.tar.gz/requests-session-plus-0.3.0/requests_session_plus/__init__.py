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
TIMEOUT: Optional[float] = 10


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
        *args,
        **kwargs,
    ):
        # TODO fix args
        """Instantiate SessionPlus object with retries and timeout enabled.

        Args:
            raise_status_exceptions (bool): Raise exceptions for status codes >=400. Defaults to False.
            retry (bool): Allow retries of failed HTTP calls. Defaults to False.
            timeout (int, None): Set a timeout for HTTP calls. Defaults to 10.
            verify (bool): Set verify=False to disable SSL verification and warnings. Defaults to True.

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
        return self._retry

    @retry.setter
    def retry(self, value: bool):
        self._retry = bool(value)
        self.update_retry()

    def update_retry(self):
        """Allow the ad-hoc update of the Retry class so we don't have to create a new SessionPlus every time.

        Args:
            retry_class (Retry, optional): (Re)set the Retry class if needed. Defaults to SessionPlusRetry.
        """
        if self._retry:
            retry = Retry(**self.retry_settings)

        else:
            retry = Retry(total=0, read=False)

        for proto, adapter in self.adapters.items():
            adapter.max_retries = retry

    @property
    def retry_backoff_factor(self) -> float:
        return self._retry_backoff_factor

    @retry_backoff_factor.setter
    def retry_backoff_factor(self, value: float):
        self._retry_backoff_factor = float(value)

    @property
    def retry_status_forcelist(self) -> List[int]:
        return self._retry_status_forcelist

    @retry_status_forcelist.setter
    def retry_status_forcelist(self, values: List[int]):
        if not isinstance(values, list):
            raise ValueError("retry_status_forcelist must be a list of integers")

        new_list: List[int] = []

        for value in values:
            new_list.append(int(value))

        self._retry_status_forcelist = new_list

    @property
    def retry_total(self) -> int:
        return self._retry_total

    @retry_total.setter
    def retry_total(self, value: int):
        self._retry_total = int(value)

    @property
    def retry_settings(self) -> Dict[str, Any]:
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
        return self._status_exceptions

    @status_exceptions.setter
    def status_exceptions(self, value: bool):
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
    def timeout(self) -> float:
        return self._timeout

    @timeout.setter
    def timeout(self, value: Optional[float]):
        if isinstance(value, (float, int, str)):
            value = float(value)
            if value <= 0.0:
                raise ValueError("timeout must be a float or integer greater than 0")

        elif value is None:
            pass

        else:
            raise ValueError("timeout must be a float or integer greater than 0")

        self._timeout = value

    @property
    def verify(self) -> bool:
        return self._verify

    @verify.setter
    def verify(self, value: bool):
        self._verify = bool(value)

        key: str = "default" if self._verify else "ignore"
        pop_filters: List[int] = []
        filter_found: bool = False

        for i, warn in enumerate(warnings.filters):
            if warn[2] == HTTPWarning:
                if warn[0] == key:
                    filter_found = True
                else:
                    print(f"{warn[0]} - {warn[2]} - needs to be removed")
                    pop_filters.append(i)

        if pop_filters:
            pop_filters.reverse()
            for filter_index in pop_filters:
                warnings.filters.pop(filter_index)

        if not filter_found:
            warnings.simplefilter(key, HTTPWarning)

    def send(self, request, **kwargs):

        if not kwargs.get("timeout") and self.timeout:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
