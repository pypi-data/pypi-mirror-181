"""Make HTTP interactions easier."""
import functools

from yarl import URL

from .auth import HTTPBasicAuth
from .core import HTTPRequest


@functools.lru_cache(maxsize=None)
def http(url: str, username: str = None, password: str = None) -> HTTPRequest:
    """
    Return driver to talk with ikscale API.

    :param url: Ikomia scale api url
    :param username: Username for authentication
    :param password: Password for authentication
    :return: A fully loaded HTTPRequest object.
    """
    # Parse url from str as yarl URL
    parsed_url = URL(url)

    # Get auth
    auth = HTTPBasicAuth(parsed_url, username, password)

    # Return HTTPRequest object
    return HTTPRequest(parsed_url, auth=auth)
