"""tests/test_SessionPlus.py

All of the features we are using are already part of requests/urllib3 so we don't have to make external calls to
test every feature.  Instead we can just make sure classes and methods are updated as intended and trust that requests/
urllib3 are working as intended.
"""


from typing import List

import pytest

from requests_session_plus import RETRY_BACKOFF_FACTOR, RETRY_STATUS_FORCELIST, RETRY_TOTAL, TIMEOUT, SessionPlus


def retry_check(session: SessionPlus) -> bool:
    protos = ["http://", "https://"]

    if session.retry:
        values = session.retry_settings
    else:
        values = {"total": 0, "read": False}

    for proto in protos:
        retry_obj = session.adapters[proto].max_retries
        for k, v in values.items():
            assert retry_obj.__dict__[k] == v


def status_exceptions_check(session: SessionPlus) -> bool:
    assert "response" in session.hooks

    found_hook: bool = False
    hook_name: str = SessionPlus._status_exception_response_hook.__name__

    for hook in session.hooks["response"]:
        if hook.__name__ == hook_name:
            found_hook = True
            break

    assert session.status_exceptions == found_hook


def test_retry():
    session = SessionPlus(retry=False)

    retry_check(session)

    session.retry = False
    assert not session.retry
    retry_check(session)

    new_backoff_factor: float = RETRY_BACKOFF_FACTOR + 1
    session.retry_backoff_factor = new_backoff_factor
    assert session.retry_backoff_factor == new_backoff_factor

    new_status_forcelist: List[int] = RETRY_STATUS_FORCELIST.copy()
    new_status_forcelist.pop(0)
    session.retry_status_forcelist = new_status_forcelist
    assert session.retry_status_forcelist == new_status_forcelist

    new_total: int = RETRY_TOTAL + 1
    session.retry_total = new_total
    assert session.retry_total == new_total

    session.retry = True
    assert session.retry
    retry_check(session)


def test_retry_extra_args():
    """Validate namespaced arguments are presented in retry_settings dictionary."""
    retry_key_1 = "retry_init_test"
    retry_val_1 = "this is an init arg"

    retry_key_2 = "retry_post_init"
    retry_val_2 = "this is a post init arg"

    bad_retry_arg = "bad_retry_arg"
    bad_retry_val = "this should not show up"

    session = SessionPlus(retry_init_test=retry_val_1, bad_retry_arg=bad_retry_val)
    session.retry_post_init = retry_val_2

    for k, v in [(retry_key_1, retry_val_1), (retry_key_2, retry_val_2)]:

        assert k not in session.retry_settings.keys()

        k = k.replace("retry_", "")

        assert k in session.retry_settings
        assert session.retry_settings[k] == v

    assert bad_retry_arg not in session.__dict__.keys()
    assert bad_retry_arg not in session.retry_settings.keys()
    assert bad_retry_val not in session.retry_settings.values()


def test_retry_validation():
    session = SessionPlus()

    for value in [100, "taco", ["taco"]]:

        with pytest.raises(ValueError):
            SessionPlus(retry_status_forcelist=value)

        with pytest.raises(ValueError):
            session.retry_status_forcelist = value


def test_status_exceptions():
    """Validate the response hook is configured correctly."""

    session = SessionPlus(status_exceptions=True)

    # make sure the response hook exists
    assert session.status_exceptions
    status_exceptions_check(session)

    # enable it a few times to make sure we don't keep appending to hook list
    pre_count = len(session.hooks["response"])

    session.status_exceptions = True
    session.status_exceptions = True
    session.status_exceptions = True
    assert session.status_exceptions
    status_exceptions_check(session)
    assert pre_count == len(session.hooks["response"])

    # make sure we can disable it
    session.status_exceptions = False
    assert not session.status_exceptions
    status_exceptions_check(session)

    # re-enable just to make sure we can set it on instantiation as well as toggle it
    session.status_exceptions = True
    assert session.status_exceptions
    status_exceptions_check(session)


def test_timeout_validation():
    session = SessionPlus()

    assert session.timeout == TIMEOUT

    session.timeout = 300
    assert session.timeout == 300

    session.timeout = None
    assert session.timeout is None

    for value in [-1, 0, "0", "taco", [], [1, 2, 3], {}]:
        with pytest.raises(ValueError):
            SessionPlus(timeout=value)

        with pytest.raises(ValueError):
            session.timeout = value
