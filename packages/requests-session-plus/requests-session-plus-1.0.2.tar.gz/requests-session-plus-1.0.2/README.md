# requests-session-plus

Drop in replacement for [requests.Session()](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) with some quality of life enhancements.

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

```

[![build](https://github.com/chambersh1129/requests-session-plus/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/chambersh1129/requests-session-plus/actions/workflows/build.yml?query=branch%3Amain)
[![coverage](https://img.shields.io/codecov/c/github/chambersh1129/requests-session-plus/main)](https://app.codecov.io/gh/chambersh1129/requests-session-plus)
![pypi](https://img.shields.io/badge/pypi-1.0.2-blue)
![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![license](https://img.shields.io/badge/license-GNUv3-green)
![code style](https://img.shields.io/badge/code%20style-black-black)


# Installing requests_session_plus

requests_session_plus is available on PyPI:

```console
$ python -m pip install requests_session_plus
```

# Comparison to Requests Session Class

All of these features are currently available in the standard requests Session class with some configuration/modification.  The goal of SessionPlus is to make the more easily accessible.

Feature | Session() | SessionPlus() |
--- | --- | ---
Default HTTP(S) Call Timeout | 0 | 10 |
HTTP(S) Timeout Set | per call | globally and per call | |
Disable Certificate Verification | per call | globally and per call |
Disable Certificate Verification Warnings | no | yes |
Raise Exceptions For Client/Server Issues | no | yes |
Retry Count | 0 | 5 |
Retry Backoff Factor | 0 | 2 |
Retry For Status Codes | 413, 429, 503 | 413, 429, 500, 502-504 |

Timeouts and certificate verification are enabled by default in SessionPlus, the others disabled.  All features can be enabled/disabled ad hoc as needed.

# Usage

SessionPlus can be used in the exact same way as a [requests Session object](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) so I'm going to rely on their documentation for most use cases.  In the following sections I'll just go over the benefits of each feature this package utilizes and how to enable/disable/modify them.

To make the most out of this package and its features you should have a strong understanding of your HTTP endpoints and how each feature could help.  Some suspiciously specific examples that I may or may not have run into:

- Making API calls to an internal network appliance where tacacs occasionally fails?
    - Disable certificate verification
    - Enable retries
    - Add 401 to "retry_status_forcelist" parameter
- Is there an API endpoint hosted in Kubernetes where aggressive health checks recycle the containers leading to occasional 502 Bad Gateway responses?
    - Enable retries
- Is there an API endpoint that has a habit of either responding quickly or getting hung and not responding at all?
    - Enable retries
    - Set the timeout to be a little higher than its average response time (if 10 second default isn't sufficient)
- Is there a cheeky developer who likes to use quirky or non-standard HTTP status codes (such as 418 I'm a Teapot) for client/server issues?
    - Enable status exceptions which raises an exception for any status code >=400
    - You can also enable retries and expand the "retry_status_forcelist" parameter
        - Any status code in "retry_status_forcelist" will issue retries
        - All other status codes >=400 will raise an exception
        - Example: lets retry 418, but don't bother retrying for 411

## Certificate Verification

This is enabled by default in both the default Session class and SessionPlus.  SessionPlus just provides an easy way to toggle it on and off globally.

It is not recommended to disable certificate verification but useful when working with HTTP endpoints which use a self-signed certificate or have some other certificate issue.  It both disables the [certificate check](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification) but also disables the warnings that bark at you when you disable certificate checks.

**NOTE:** If [retries](#retries) are also enabled, retries will be issued for HTTP calls to servers that have bad certificates.

## Configuring Certificate Verification

Parameter:
 - verify : boolean : verify certificate or not. Defaults to True

```python
>>> from requests_session_plus import SessionPlus
>>> s = SessionPlus()  # enabled by default
>>> s = SessionPlus(verify=False)  # disable certificate verification
```

Certificate verification can be toggled on/off

```python
>>> s = SessionPlus()  # enabled by default
>>> s.verify = False  # temporarily disable it
>>> # ... make 1 or more HTTP call to server with a bad certificate ...
>>> s.verify = True  # re-enable and continue
```

Making an HTTP call to server with a bad cert

```python
>>> s = SessionPlus()
>>> s.get("https://self-signed.badssl.com/")
# ... output compressed ...
# SSLError exception thrown
requests.exceptions.SSLError: HTTPSConnectionPool(host='self-signed.badssl.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLcertificateVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:997)')))
>>>
```

Same results with retries enabled, it just takes longer as retries are performed with increasing backoff timer

```python
>>> s = SessionPlus(retry=True)
>>> s.get("https://self-signed.badssl.com/")
# ... output compressed ...
# SSLError exception thrown after 5 retries (default retry total)
requests.exceptions.SSLError: HTTPSConnectionPool(host='self-signed.badssl.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:997)')))
```

If we utilize the requests way of disabling certificates, we get warnings

```python
>>> s = SessionPlus()
>>> s.get("https://self-signed.badssl.com/", verify=False)  # disable certificate verification
# warnings are thrown
/home/chambersh1129/Documents/code/personal/requests-session-plus/venv/lib/python3.10/site-packages/urllib3/connectionpool.py:1045: InsecureRequestWarning: Unverified HTTPS request is being made to host 'self-signed.badssl.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
# but no exception is thrown
<Response [200]>
```

Now we can try it the SessionPlus way.  No exceptions, no warnings

```python
>>> s = SessionPlus(verify=False)
>>> s.get("https://self-signed.badssl.com/")
<Response [200]>
```

## Client/Server Error Exceptions

This is disabled by default in both the default Session class and SessionPlus and takes a few steps to enable with the default Session class.  SessionPlus just provides an easy way to toggle it on and off.

Sometimes you just want to know if the HTTP call worked or not instead of having a lot of conditionals checking the status code(s).  This setting will raise an exception if the status code is >=400.  The status code will be provided in the error message if you still want to get the status code but you will not have access to the response object.

**NOTE:** If [retries](#retries) are also enabled, certain status codes will issue a retry with a backoff timer.  These status codes are configurable with [retry_status_forcelist](#configuring-retries).

## Configuring Client/Server Error Exceptions

Parameter:
 - status_exceptions : boolean : whether exceptions should be raised or not. Defaults to False

```python
>>> from requests_session_plus import SessionPlus
>>> s = SessionPlus()  # disabled by default
>>> s = SessionPlus(status_exceptions=True)  # rase exception for status codes >= 400
```

Status exceptions can be toggled on/off

```python
>>> s = SessionPlus(status_exceptions=True)  # raise exceptions
>>> s.status_exceptions = False  # disable temporarily
>>> # ... make HTTP call we want response object regardless of status code ...
>>> s.status_exceptions = True  # back to raising exceptions for status codes >= 400
```

An example, with status_exceptions and retries enabled.

```python
>>> s = SessionPlus(status_exceptions=True, retries=True)
>>> s.get("https://httpstat.us/418/")  # 418 I'm a teapot
# ... output compressed ...
# HTTPError exception thrown without retries
requests.exceptions.HTTPError: 418 Client Error: Im a teapot for url: https://httpstat.us/418/
```

In the above case, retries were not used because 418 was not in the default [retry_status_forcelist](#configuring-retries).  We can try again with a status code that is in the list.

```python
>>> s = SessionPlus(status_exceptions=True, retries=True)
>>> s.get("https://httpstat.us/429/")  # 429 Too Many Requests
# ... output compressed ...
# RetryError exception thrown after 5 retries (default)
requests.exceptions.RetryError: HTTPSConnectionPool(host='httpstat.us', port=443): Max retries exceeded with url: /429/ (Caused by ResponseError('too many 429 error responses'))
```

If we disable retries, we are back to the HTTPError we got with the 418.

```python
>>> s = SessionPlus(status_exceptions=True)
>>> s.get("https://httpstat.us/429/")  # 429 Too Many Requests
# ... output compressed ...
# HTTPError exception thrown without retries, same as the 418 above
requests.exceptions.HTTPError: 429 Client Error: Too Many Requests for url: https://httpstat.us/429/
```

## Retries

The default Session class does not perform retries, and when enabled a backoff of 0 is set meaning it does not wait between HTTP calls.

Retries are helpful if the server uptime is spotty and the calls are idempotent.  Instead of setting a loop to try/fail/sleep/repeat (or worse, try/fail/break), SessionPlus will enable retries with some [helpful defaults](#configuring-retries).

## When are Retries Performed?

If retries are enabled, they will be used for:
 - TimeoutErrors when timeoutes are enabled
 - SSLErrors when verify=True
 - HTTP status codes >=400 when status_exceptions=True
 - For certain status codes set in retry_status_forcelist, even if status_exceptions=True

 The default status codes configured for retries in SessionPlus are:

 - [413 Payload Too Large](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/413)
 - [429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429)
 - [500 Internal Server Error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500)
 - [502 Bad Gateway](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/502)
 - [503 Service Unavailable](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/503)
 - [504 Gateway Timeout](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/504)

## How long will Retries Take?

There is a formula to determine how long to wait between retries (found in the [Retry docs](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry)):

```
{backoff factor} * (2 ** ({number of total retries} - 1))
```

Example #1
- Parameters
    - backoff_factor = 2 (SessionPlus default)
    - total = 5 (SessionPlus default)
    - timeout = 10 (SessionPlus default)
    - server responds immediately with a 429 Too Many Requests so timeout does not come into play
- Retries will be sent at
    - 2s after the first failure
    - 4s after the second failure
    - 8s after the third failure
    - 16s after the fourth failure
    - 32s after the fifth failure

A total of 62 seconds is spent trying to get a response.  The Too Many Requests issue might be resolved by then.

Example #2
- Parameters
    - backoff_factor = 2 (SessionPlus default)
    - total = 5 (SessionPlus default)
    - timeout = 10 (SessionPlus default)
    - server takes >10 seconds to respond
- Retries will be sent at
    - 10s timeout + 2s after the first failure
    - 10s timeout + 4s after the second failure
    - 10s timeout + 8s after the third failure
    - 10s timeout + 16s after the fourth failure
    - 10s timeout + 32s after the fifth failure
    - requests.exceptions.ReadTimeout exception is raised

A total of 112 seconds is spent trying to get a response.  In this case, [disabling or increasing the timeout](#configuring-timeouts) could be useful.

Example #3
- Parameters
    - backoff_factor = 10 (5x increase over SessionPlus default)
    - total = 5 (SessionPlus default)
    - timeout = 10 (SessionPlus default)
    - server responds immediately with a 503 Service Unavailable
- Retries will be sent at
    - 10s after the first failure
    - 20s after the second failure
    - 40s after the third failure
    - 80s after the fourth failure
    - 160s after the fifth failure

A total of 310 seconds is spent trying to get a response.  The Server Unavailable issue might be resolved by then.

## Configuring Retries

SessionPlus sets defaults for 3 specific parameters and there is a fourth parameter to enable/disable retries.  You can pass additional parameters for the retries by prepending "retry_" to them, a full list can be found in the [urllib3 Retry docs](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry).

**NOTE**: Before altering the default values below be concious of how long the worst case HTTP call will take.  These defaults were chosen so the maximum time waiting for all retries is between 62 seconds (if server responds immediately) and 112 seconds (if timeouts are hit).  Increasing these values for performance or latency senstive applications could lead to issues.

Parameter:
 - retry : bool : enable or disable retry functionality. Defaults to False
 - retry_backoff_factor : float : used in the formula to determine how long to wait before retrying.  Defaults to 2
 - retry_status_forcelist : list : HTTP status codes to retry. Defaults to [413, 429, 500, 502, 503, 504]
 - retry_total: int : total number of retries before failing. Defaults to 5

```python
>>> from requests_session_plus import SessionPlus
>>> s = SessionPlus()  # retries disabled by default
>>> s = SessionPlus(retry=True)  # enable retries
```

Retries can be toggled on/off

```python
>>> s = SessionPlus(retry=True)
>>> s.retry = False  # retries are disabled
>>> # ... make HTTP call where retries aren't needed ...
>>> s.retry = True  # re-enable retries
```

Viewing/Changing Retry Settings

```python
>>> s = SessionPlus(retry=True)
>>> # view the settings
>>> s.retry_settings
{'backoff_factor': 2, 'status_forcelist': [413, 429, 500, 502, 503, 504], 'total': 5}
>>> # modify a default setting
>>> s.retry_total = 10
>>> s.retry_backoff_factor = 5
>>> s.retry_settings
{'backoff_factor': 5.0, 'status_forcelist': [413, 429, 500, 502, 503, 504], 'total': 10}
>>> # passing in new Retry settings.  Note: no validation is done for those not listed above in Parameters
>>> s.retry_raise_on_status = False
>>> s.retry_settings
{'backoff_factor': 5.0, 'status_forcelist': [413, 429, 500, 502, 503, 504], 'total': 10, 'raise_on_status': False}
>>> # initialize new session with all of these settings
>>> new_session = SessionPlus(retry=True, retry_raise_on_status=False, retry_total=10, retry_backoff_factor=5)
>>> new_session.retry_settings
{'backoff_factor': 5.0, 'status_forcelist': [413, 429, 500, 502, 503, 504], 'total': 10, 'raise_on_status': False}
>>> # settings persist, even when retries are disabled
>>> new_session.retry = False
>>> new_session.retry_settings
```

For the retry settings to be completed updated, you need to run .update_retry().  This is done automatically when enabling/disabling retries, this is just a helper method to run if you need to change an existing enabled retry.

```python
>>> s = SessionPlus(retry=True)
>>> s.retry_settings
{'backoff_factor': 2, 'status_forcelist': [413, 429, 500, 502, 503, 504], 'total': 5}
>>> # update the settings
>>> s.retry_total = 10
>>> s.retry_settings
{'backoff_factor': 2, 'status_forcelist': [413, 429, 500, 502, 503, 504], 'total': 10}
>>> # apply the settings
>>> s.update_retry()
```

For the parameters SessionPlus has defaults for, there is also input validation.  Other parameters are passed straight to the Retry object.

```python
>>> s = SessionPlus(retry=True)
>>> s.retry_status_forcelist = 429
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/chambersh1129/Documents/code/personal/requests-session-plus/requests_session_plus/__init__.py", line 68, in __init__
    self.retry_status_forcelist = retry_status_forcelist
  File "/home/chambersh1129/Documents/code/personal/requests-session-plus/requests_session_plus/__init__.py", line 123, in retry_status_forcelist
    raise ValueError("retry_status_forcelist must be a list of integers")
ValueError: retry_status_forcelist must be a list of integers
>>>
>>> s.retry_read = "this should be an integer"
>>> s.update_retry()
>>> s.get("https://httpstat.us/429/")  # 429 Too Many Requests
# ... output compressed ...
# TypeError exception thrown when first retry is attempted
TypeError: '<' not supported between instances of 'str' and 'int'
```

## Timeouts

Some HTTP calls should only take X amount of time, and if it takes longer the server is likely hung or some other issue.  Timeouts allow you to set a maximum time to wait before declaring the server unresponsive and moving on.

The default Session class supports timeouts per HTTP call, SessionPlus just provides the ability to set it globally in addition to per call.

## Configuring Timeouts

Parameter:
 - timeout : [float,None] : how long to wait, in seconds, before raising an exception. Defaults to 10

```python
>>> from requests_session_plus import SessionPlus
>>> s = SessionPlus()  # timeout set to 10 seconds
>>> s = SessionPlus(timeout=None)  # disable the timeout
```

Global Timeout can be toggled on/off

```python
>>> s = SessionPlus()  # timeout set to 10 seconds
>>> s.timeout = None  # now no call has a timeout
>>> # ... make a really long HTTP call ...
>>> s.timeout = 30  # set it back to whatever you want
```

You can still overwite it per call and the default value is maintained for future calls

```python
>>> s = SessionPlus(timeout=1)
>>> s.get("https://httpstat.us/200/?sleep=1250")  # 200 OK that takes 1.25 seconds to respond
# ... ouput compressed ...
# TimeoutError triggers a ReadTimeoutError which triggers a MaxRetryError and eventually a ConnectionError
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='httpstat.us', port=443): Max retries exceeded with url: /200/?sleep=1250 (Caused by ReadTimeoutError("HTTPSConnectionPool(host='httpstat.us', port=4
43): Read timed out. (read timeout=1.0)"))
>>>
>>> # disable retries and try again
>>> s.retry = False
# ... output compressed ...
# TimeoutError triggers a ReadTimeoutError which triggers a ReadTimeout
requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='httpstat.us', port=443): Read timed out. (read timeout=1.0)
>>>
>>> # increase the timeout for this call only
>>> s.timeout
1.0
>>> # make the call again, overwriting global timeout
>>> s.get("https://httpstat.us/200/?sleep=1250", timeout=2)  # 200 OK that takes 1.25 seconds to respond
<Response [200]>
>>> # global is unchanged
>>> s.timeout
1.0
```

**NOTE:** Once again, disabling timeouts isn't a silver bullet.  Other timeouts come into play, both at the python level (urllib3 timeouts, socket timeouts) or at the server level (NGINX proxy_read_timeout for example).  Setting timeout=None for an HTTP call does not guarantee exceptions aren't raised.
