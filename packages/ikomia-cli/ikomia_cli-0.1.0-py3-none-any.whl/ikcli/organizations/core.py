"""Organization API Objects."""
from yarl import URL

from ikcli.net.api import List, Object
from ikcli.net.http.core import HTTPRequest
from ikcli.users.core import User


class Member(Object):
    """Organization Member API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of Member object.

        :return: Member object representation
        """
        return f"{self['username']} as {self['role']}"


class Members(List):
    """Member API List."""

    def __init__(self, http: HTTPRequest, url: URL):
        super().__init__(http, url, Member)

    def create(self, user: User = None, **kwargs) -> Member:
        return super().create(user=user["url"], **kwargs)


class Organization(Object):
    """Organization API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of Organization object.

        :return: Organization object representation
        """
        return f"Organization {self['name']}"

    @property
    def members(self) -> Members:
        """
        Return organization member list.

        :return: Member list
        """
        return Members(self._http, self._url / "members/")


class Organizations(List):
    """Organization API List."""

    def __init__(self, http: HTTPRequest):
        super().__init__(http, URL("/v1/organizations/"), Organization)
