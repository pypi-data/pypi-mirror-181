"""Namespace API Object."""
from yarl import URL

from ikcli.net.api import List, Object
from ikcli.net.http.core import HTTPRequest
from ikcli.projects.core import Projects


class Namespace(Object):
    """Namespace API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of Namespace object.

        :return: Namespace object representation
        """
        return f"Namespace {self['path']}"

    @property
    def projects(self) -> Projects:
        """
        Return a namespace project list.

        :return: Namespace project list
        """
        return Projects(self._http, self._url / "projects/")

    @property
    def namespaces(self) -> "Namespace":
        """
        Return sub namespace list.

        :return: Sub namespace list
        """
        return Namespaces(self._http, self._url / "namespaces/")


class Namespaces(List):
    """Namespace API List."""

    def __init__(self, http: HTTPRequest, url: URL = None):
        if url is None:
            url = URL("/v1/namespaces/")
        super().__init__(http, url, Namespace)
