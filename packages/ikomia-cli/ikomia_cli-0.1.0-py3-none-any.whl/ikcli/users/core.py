"""User API object."""
import random
import string

from yarl import URL

from ikcli.net.api import List, Object
from ikcli.net.http.core import HTTPRequest


class User(Object):
    """User API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of User object.

        :return: User object representation
        """
        return f"User {self['username']}"


class Users(List):
    """User API List."""

    def __init__(self, http: HTTPRequest):
        super().__init__(http, URL("/v1/users/"), User)


class Account(Object):
    """Manage personal account."""

    def __init__(self, http: HTTPRequest):
        super().__init__(http, URL("/v1/accounts/"))

    def login(self, username: str, password: str):
        """
        Log user to platform.

        :param username: User name
        :param password: User password
        """
        # Fake endpoint until authentication works for real
        letters = string.ascii_uppercase + string.digits
        token = "".join(random.choice(letters) for i in range(29))
        print(f"export IKCLI_TOKEN='IKT{token}'")

    def logout(self):
        """Log out user."""
        self._http.post(self._url / "logout/")

    def register(self, username, email, password, password2=None) -> User:
        """
        Register a new user.

        :param username: User name
        :param email: User email
        :param password: User password
        :param password2: User password verification
        :return: Newly created user
        """
        if password2 is None:
            password2 = password
        data = {
            "username": username,
            "email": email,
            "password": password,
            "password2": password2,
        }
        response = self._http.post(self._url / "register/", data)
        return User(self._http, URL(response["url"]), data=response)
