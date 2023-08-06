# requests-session-plus

Drop in replacement for requests.Session() with some quality of life enhancements.

```python
>>> from requests_session_plus import SessionPlus  # equivalent to "from requests import Session"
>>> s = SessionPlus()
>>> r = s.get("https://httpbin.org/basic-auth/user/pass", auth=("user", "pass"))
>>> r.status_code
200
>>> r.headers["content-type"]
'application/json'
>>> r.encoding
'utf-8'
>>> r.text
'{\n  "authenticated": true, \n  "user": "user"\n}\n'
>>> r.json()
{'authenticated': True, 'user': 'user'}
```

[![build](https://github.com/chambersh1129/requests-session-plus/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/chambersh1129/requests-session-plus/actions/workflows/build.yml?query=branch%3Amain)
[![coverage](https://img.shields.io/codecov/c/github/chambersh1129/requests-session-plus/main)](https://app.codecov.io/gh/chambersh1129/requests-session-plus)
![pypi](https://img.shields.io/badge/pypi-0.2.1-blue)
![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![license](https://img.shields.io/badge/license-GNUv3-green)
![code style](https://img.shields.io/badge/code%20style-black-black)

# Installing requests_session_plus

requests_session_plus is available on PyPI:

```console
$ python -m pip install requests_session_plus
```

# Comparison to requests.Session()

Feature | Session() | SessionPlus() | Note |
--- | --- | --- | ---
Default HTTP(S) Call Timeout | 0 | 5 | |
Default Retry Count | 0 | 3 | |
Default Retry Backoff Factor | 0 | 2.5 | |
Disable Cert Verification | per call | globally, per call | disabled in SessionPlus by default |
Disable Cert Verification Warnings | :x: | :heavy_check_mark: | disabled in SessionPlus by default |
HTTP(S) Timeout Set | per call | globally, per call | | 
Raise Exceptions For Client/Server Issues | :x: | :heavy_check_mark: |  disabled in SessionPlus by default |
Retry For Status Codes | 413, 429, 503 | 413, 429, 500, 502-504 | |

Retries and timeouts are very useful so they are enabled by default in SessionPlus.  The other features can be easily enabled by passing a boolean on instantiation.

# Usage

SessionPlus can be used in the exact same way as [requests.Session](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) so I'm going to rely on their documentation for most use cases.  In the following sections I'll just go over the benefits of each feature and how to disable or modify them.

## Retries
Retries are helpful if the server uptime is spotty and the calls are idempotent.  Instead of setting a loop to try/fail/sleep/repeat (or worse, try/fail/break), this package will enable retries with some [common sense defaults](#overwriting-retry-parameters).  The default Session class does not perform retries, and if you simply enable it there is no backoff meaning it does not wait in between HTTP calls.

There is a formula to determine how long to wait between retries

```
{backoff factor} * (2 ** ({number of total retries} - 1))
```

Some examples
- Example #1
    - Parameters
        - backoff_factor = 2.5 (SessionPlus default)
        - total = 5 (SessionPlus default)
        - timeout = 5 (SessionPlus default)
        - server responds immediately with a 429 Too Many Requests so timeout does not come into play
    - Retries will be sent at 
        - 2.5s after the first failure
        - 5s after the second failure
        - 10s after the third failure
        - 20s after the fourth failure
        - 40s after the fifth failure
    - A total of 77.5 seconds is spent trying to get a response
    - The Too Many Requests issue might be resolved by then
- Example #2
    - parameters
        - backoff_factor = 2.5 (SessionPlus default)
        - total = 5 (SessionPlus default)
        - timeout = 5 (SessionPlus default)
        - server takes >5 seconds to respond
    - Retries will be sent at 
        - 5s timeout + 2.5s after the first failure
        - 5s timeout + 5s after the second failure
        - 5s timeout + 10s after the third failure
        - 5s timeout + 20s after the fourth failure
        - 5s timeout + 40s after the fifth failure
        - requests.exceptions.ReadTimeout exception is raised
    - for a total of 32.5 seconds trying to get a response
- Example #2
    - parameters
        - backoff_factor = 1.5 (lower than SessionPlus default)
        - total = 5 (higher than SessionPlus default)
        - timeout = 5 (SessionPlus default)
    - Retries will be sent at 
        - 1.5s after the first failure
        - 3s after the second failure
        - 6s after the third failure
        - 12s after the fourth failure
        - 24s after the fifth failure
    - for a total of 46.5 seconds trying to get a response
- Example #1
    - parameters
        - backoff_factor = 2.5 (SessionPlus default)
        - total = 3 (SessionPlus default)
        - timeout = 5 (SessionPlus default)
    - Retries will be sent at 
        - 5s timeout + 2.5s after the first failure
        - 5s timeout + 5s after the second failure
        - 5s timeout + 10s after the third failure
    - for a total of 32.5 seconds trying to get a response
- Example #2
    - parameters
        - backoff_factor = 1.5 (lower than SessionPlus default)
        - total = 5 (higher than SessionPlus default)
        - timeout = 5 (SessionPlus default)
    - Retries will be sent at 
        - 5s timeout + 1.5s after the first failure
        - 5s timeout + 3s after the second failure
        - 5s timeout + 6s after the third failure
        - 5s timeout + 12s after the fourth failure
        - 5s timeout + 24s after the fifth failure
    - for a total of 71.5 seconds trying to get a response

[Disabling timeoutes](#disabling-timeout) in SessionPlus will only increase the time it takes for failures, as it will default to whatever urllib3 has set.

### Disabling Retries

Parameter:
 - retry : Retry or None : requests_session_plus.retries.SessionPlusRetry

```python
>>> from requests_session_plus import SessionPlus
>>> s = SessionPlus(retry=None)
```

### Overwriting Retry Parameters
requests_session_plus comes with a custom SessionPlusRetry class that inherits from urllib3.util.retry.Retry similar to how SessionPlus inherits from Session.  A full list of parameters can be found in the [Retry API documentation](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry).  The parameters and their defaults that SessionPlusRetry class use are below.

Parameter:
 - backoff_factor : float : used in the formula to determine how long to wait before retrying : default=2.5
 - status_forcelist : list : HTTP status codes to retry : default=[413, 429, 500, 502, 503, 504]
 - total: int : total number of retries before failing : default=3

Overwriting parameters
```python
>>> from requests_session_plus import SessionPlus
>>> from requests_session_plus.retries import SessionPlusRetry
>>> r = SessionPlusRetry(total=5, backoff_factor=1.0)
>>> s = SessionPlus(retry=r)
```

Retries are applied to the HTTPAdapter so at this time they cannot be toggled/overwritten per call.  If you need to make an individual call without retries enabled, it is recommended to just use a standard [request.request](https://requests.readthedocs.io/en/latest/api/#requests.request) or [request.Session](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) and switch back to SessionPlus when you need retries once again, or you can use a second SessionPlus object with retries disabled.  It entirely depends on your use case.

## Timeouts
There may be a case where 

### Disabling Timeout

### Overwriting Timeout Value

## Raising Exceptions for Client/Server Errors
Sometimes you just want to know if it worked or not instead of having a lot of if statements checking the status code.  This will raise an exception if the status code is >=400.  The status code will be provided in the error message if you still want to get the status code but you will not have access to the response object.

This is disabled by default in SessionPlus, but can be useful for some HTTP Calls.

### Enabling Client/Server Error Exceptions

Parameter:
 - raise_status_exceptions : boolean : default=False

```python
>>> from requests_session_plus import SessionPlus
>>> s = SessionPlus(raise_status_exceptions=True)
```

## Certificate Verification
This is not recommended, but often working with internal tools with self signed certs I find myself needing it.  It both disables the [certificate check](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification) but also disables the warnings that bark at you when you disable this.

### Enabling Certificate Verification

Parameter:
 - allow_insecure : boolean : default=False

```python
>>> from requests_session_plus import SessionPlus
>>> s = SessionPlus(allow_insecure=False)
```