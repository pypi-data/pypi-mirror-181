"""Map data to REST urls."""
from typing import Any, Optional, Type

from yarl import URL

from ikcli.net.http.core import HTTPRequest

from .exceptions import NotUniqueObjectException, ObjectNotFoundException
from .pagination import PageNumberPagination, Pagination


class Object:
    """
    Base object to map data from REST url.

    This can be use as python dict.
    """

    def __init__(self, http: HTTPRequest, url: URL, data: dict = None):
        """
        Initialize a new api object.

        :param http: A HTTPRequest object to talk with api
        :param url: Relative or absolute URL to object
        :param data: Object data
        """
        self._http = http
        self._url = url
        if data is None:
            self._data = {}
        else:
            self._data = data

    def get(self, key: Any, default: Any = None) -> Optional[Any]:
        """
        Get object item.

        :param key: Item key
        :param default: Default value if key not found
        :return: Object item value
        """
        return self._data.get(key, default=default)

    def __getitem__(self, key: str):
        """
        Get object item.

        :param key: Item key
        :return: Object item value

        Example:
            name = organisation['name']
        """
        return self._data.get(key)

    # TODO: def __missing__(self, key)
    # as in dict, if key is missing, try to load / reload data
    # https://docs.python.org/3/reference/datamodel.html#object.__missing__

    def __setitem__(self, key: str, value):
        """
        Set object item value.

        :param key: Object item key
        :param value: Object item value
        """
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        """
        Return if object contains item.

        :param key: Object item key
        :return: True if item exists, False otherwise
        """
        return key in self._data

    def clear(self):
        """Clear object data."""
        self._data.clear()

    def delete(self):
        """
        Delete object on remote server.

        :return: Raw server response
        """
        return self._http.delete(self._url)


class List:
    """A list of API objects."""

    def __init__(
        self,
        http: HTTPRequest,
        url: URL,
        object_class: Type[Object],
        pagination: Type[Pagination] = PageNumberPagination,
    ):
        """
        Initialize a new api object list.

        :param http: A HTTPRequest object to talk with api
        :param url: Absolute or relative path to list
        :param object_class: A class to map api object in list
        :param pagination: A pagination class
        """
        self._http = http
        self._url = url
        # TODO: remove when code will be clean
        assert isinstance(url, URL)
        self._object_class = object_class
        self._pagination = pagination

    def list(self, **kwargs) -> Pagination:
        """
        Return a generator to object list.

        :param kwargs: lookup param
        :return: A pagination generator
        """
        # Remove 'None' values from kwargs (not supported by yarl as query)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return self._pagination(self._http, self._url % kwargs, self._object_class)

    def get(self, **kwargs) -> Object:
        """
        Return an object.

        :param kwargs: lookup param
        :return: An API object
        :raises ObjectNotFoundException: If no object found
        :raises NotUniqueObjectException: If more than one object found
        """
        pagination = iter(self.list(**kwargs))
        if len(pagination) == 0:
            raise ObjectNotFoundException(self._object_class, **kwargs)
        if len(pagination) > 1:
            raise NotUniqueObjectException(self._object_class, pagination, **kwargs)
        return pagination.get(0)

    def create(self, **kwargs) -> Object:
        """
        Create a new object in list.

        :param kwargs: Object data
        :return: New API Object
        """
        # Remove 'None' values from kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        data = self._http.post(self._url, data=kwargs)
        return self._object_class(self._http, URL(data["url"]), data=data)
