# Built-In
import weakref
import re
from typing import Any, TypeVar
from urllib.request import urlopen, Request
from urllib.error import URLError

_METADATA_URL = "http://metadata.google.internal/computeMetadata/v1"
T = TypeVar("T")


def add_code(exception: Exception, status_code: int) -> Exception:
    """
    Set a new attribute "status_code" this can be usefull to change the status_code from
    the fixed into the specified exception handler.
    No custom callback needed.

    :param exception: Exception to set attribute before being raised
    :param status_code: New status code to override from exception handler
    """
    if not isinstance(status_code, int):
        message = f"Status code must be an int, but is of type {type(status_code)}"
        raise TypeError(message)
    if status_code < 100 or status_code >= 600:
        message = (
            "Status code must have a value between 100 and 599, "
            f"but it has a value of {status_code}"
        )
        raise ValueError(message)
    setattr(exception, "status_code", status_code)
    return exception


def add_data(exception: Exception, data: Any) -> Exception:
    """
    Set a new attribute "data" and set any value, this can be usefull to provide extra
    content information from the content_callback

    :param exception: Exception to set attribute before being raised
    :param data: Value to set into attribute

    :return: Same exception but modified with the extra attribute
    """
    setattr(exception, "data", data)
    return exception


class InnerClassProperty:
    """
    Descriptor for making inner classes.

    Adds a property 'owner' to the inner class, pointing to the outer
    owner instance.
    """

    # Use a weakref dict to memoise previous results so that
    # instance.Inner() always returns the same inner classobj.
    def __init__(self, inner):
        self.inner = inner
        self.instances = weakref.WeakKeyDictionary()

    def __get__(self, instance, _):
        if instance is None:
            return self.inner
        if instance not in self.instances:
            self.instances[instance] = type(
                self.inner.__name__, (self.inner,), {"owner": instance}
            )
        return self.instances[instance]


def update(dict_1: dict, dict_2: dict) -> dict:
    """
    Update dict_1 with dict_2

    :param dict_1: dict to be updated
    :param dict_2: dict to update dict_1 with

    :return: dict_1
    """
    dict_1.update((k, v) for k, v in dict_2.items() if v is not None)
    return dict_1


def get_exc_name(exception: Exception) -> str:
    """
    Get the exception name

    :param exception: Exception to get the name from
    :return: Exception name
    """
    try:
        exception_class = exception.__class__
        exception_model = f"{exception_class.__module__}.".replace("builtins.", "")
        return f"{exception_model}{exception_class.__name__}"
    except AttributeError:
        return "Exception"


def get(data, pattern: str | re.Pattern, default: T | None = None) -> T | None:
    """
    Get the value from a key in a dict

    :param key: Key to get the value from
    :param data: Dict to get the value from

    :return: Value from key
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern, re.IGNORECASE)
    key = next(filter(pattern.match, data), "")
    return data.get(key, default)


def request(url: str, **kwargs) -> str:
    """
    Make a request to the specified url

    :param url: URL to make the request to
    :param kwargs: Keyword arguments to pass to the request function
    :return: Response from the request
    """
    req = Request(url, **kwargs)
    with urlopen(req) as response:  # nosec
        return response.read().decode()


def fetch(url, **kwargs) -> str | None:
    """
    Fetch data from a url

    :param url: URL to fetch data from
    :param kwargs: Keyword arguments to pass to the request function
    :return: Data from the url
    """
    try:
        return request(url, **kwargs)
    except URLError:
        return None


def fetch_metadata(endpoint: str) -> str | None:
    """
    Get the metadata from internal metadata server

    :param endpoint: Endpoint to get the metadata from
    :return: Metadata from endpoint
    """
    url = f"{_METADATA_URL}/{endpoint}"
    headers = {"Metadata-Flavor": "Google"}
    return fetch(url, headers=headers)
