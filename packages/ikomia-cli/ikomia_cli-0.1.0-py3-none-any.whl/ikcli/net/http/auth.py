"""Manage HTTP authentication methods."""
from typing import Optional

import requests
from yarl import URL


class HTTPBasicAuth(requests.auth.AuthBase):
    """Basic HTTP authentication."""

    def __init__(self, url: URL, username: Optional[str], password: Optional[str]):
        """
        Initialize authentication.

        :param url: URL to authenticate
        :param username: A user name
        :param password: A password
        """
        super().__init__()
        self.url = url
        self.username = username
        self.password = password

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        """
        Modify a request to set authentication headers.

        :param r: a Prepared Request
        :return: An authenticated and prepared request
        """
        if self.username is None or self.password is None:
            return r

        # Add header
        r.headers["Authorization"] = requests.auth._basic_auth_str(self.username, self.password)
        return r
