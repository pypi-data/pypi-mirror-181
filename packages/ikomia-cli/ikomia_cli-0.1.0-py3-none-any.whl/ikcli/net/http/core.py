"""Core HTTP object."""
import logging

import requests
import requests.auth
from yarl import URL

from .exceptions import HTTPBadCodeError
from .serializer import JsonSerializer, Serializer, load

logger = logging.getLogger(__name__)


# TODO: reduce this timeout be finding way to make thins async
DEFAULT_TIMEOUT = 15 * 60 * 60


class HTTPRequest:
    """An object to make requests usage easier."""

    def __init__(self, url: URL, auth=None, timeout: int = DEFAULT_TIMEOUT, serializer: Serializer = None):
        """
        Initialize HTTPRequest object.

        :param url: IKScale service url
        :param auth: Authentication class
        :param timeout: HTTP request timeout
        :param serializer: A Serializer to format data before request. If None, use JsonSerializer
        """
        # TODO: remove when code will be clean
        assert isinstance(url, URL)
        self.url = url
        self.timeout = timeout
        self.connect_timeout = 5
        self.auth = auth
        self.session = requests.Session()
        self.headers = {"User-Agent": "IkomiaCli"}
        if serializer is None:
            self.serializer = JsonSerializer()
        else:
            self.serializer = serializer

    def request(self, method: str, path: URL, query: dict = None, data=None, files: dict = None):
        """
        Send an HTTP request.

        :param method: HTTP method
        :param path: Query path as URL
        :param query: URL query params
        :param data: Data to send
        :param files: A dict that contains (filename, fh) pair
        :return: A tuple with raw content and headers
        :raises HTTPBadCodeError: If server return a code <200 or >299
        :raises requests.exceptions.ReadTimeout: If request timeout
        """
        # Prepare headers
        headers = self.headers.copy()

        # TODO: remove when code will be clean
        assert isinstance(path, URL)

        # Check if url is absolute
        if path.is_absolute():
            # Assert then address same origin
            assert path.origin() == self.url, f"Given URL '{path}' is not relative with '{self.url}'"
            url = path
        else:
            url = self.url.join(path)

        if data is not None:
            data = self.serializer.dump(data)
            headers["Content-Type"] = format(self.serializer.mime)

        # Create request object
        request = requests.Request(
            method=method,
            url=url,
            headers=headers,
            params=query,
            data=data,
            files=files,
            auth=self.auth,
        )
        prepared_request = self.session.prepare_request(request)

        # Produce some debug logs
        logger.debug("Will %s '%s'", prepared_request.method, prepared_request.url)
        if prepared_request.headers:
            logger.debug(" with headers : %s", prepared_request.headers)
        if prepared_request.body:
            if len(prepared_request.body) > 2048:
                logger.debug(" with body    : .... too long to be dumped ! ...")
            else:
                logger.debug(" with body    : %s", prepared_request.body)

        # Get response
        try:
            response = self.session.send(
                prepared_request, timeout=(self.connect_timeout, self.timeout), allow_redirects=False
            )
        except requests.exceptions.ReadTimeout:
            logger.warning(
                "'%s' '%s' timeout after %d seconds", prepared_request.method, prepared_request.url, self.timeout
            )
            # TODO: raise custom exception ?
            raise

        logger.debug("Response code : %d", response.status_code)
        logger.debug(" with headers : %s", response.headers)
        if ("Content-Length" in response.headers and int(response.headers["Content-Length"]) > 10240) or len(
            response.content
        ) > 2048:
            logger.debug(" with content    : .... too long to be dumped ! ...")
        else:
            logger.debug(" with content    : %s", response.content)

        # 200 = return response and meta
        # TODO = response.raise_for_status()
        if response.status_code >= 200 and response.status_code <= 299:
            return (response.content, response.headers)

        # Otherwise raise error
        raise HTTPBadCodeError(
            prepared_request.url, response.status_code, headers=response.headers, content=response.content
        )

    def head(self, path: URL, query: dict = None):
        """
        HEAD HTTP Request.

        :param path: request path
        :param query: Query param as dict
        :return: Python data
        """
        (content, metadata) = self.request("HEAD", path, query=query)
        return load(content, metadata=metadata)

    def get(self, path: URL, query: dict = None):
        """
        GET HTTP Request.

        :param path: request path
        :param query: Query param as dict
        :return: Python data
        """
        (content, metadata) = self.request("GET", path, query=query)
        return load(content, metadata=metadata)

    def post(self, path: URL, data, files: dict = None, query: dict = None):
        """
        POST HTTP Request.

        :param path: request path
        :param data: Payload data
        :param files: A dict that contains info about files to send
        :param query: Query param as dict
        :return: Python data
        """
        (content, metadata) = self.request("POST", path, query=query, data=data, files=files)
        return load(content, metadata=metadata)

    def put(self, path: URL, data, files: dict = None, query: dict = None):
        """
        PUT HTTP Request.

        :param path: request path
        :param data: Payload data
        :param files: A dict that contains info about files to send
        :param query: Query param as dict
        :return: Python data
        """
        (content, metadata) = self.request("PUT", path, query=query, data=data, files=files)
        return load(content, metadata=metadata)

    def patch(self, path: URL, data, files: dict = None, query: dict = None):
        """
        PATCH HTTP Request.

        :param path: request path
        :param data: Payload data
        :param files: A dict that contains info about files to send
        :param query: Query param as dict
        :return: Python data
        """
        (content, metadata) = self.request("PATCH", path, query=query, data=data, files=files)
        return load(content, metadata=metadata)

    def delete(self, path: URL, query: dict = None):
        """
        DELETE HTTP Request.

        :param path: request path
        :param query: Query param as dict
        :return: Python data
        """
        (content, metadata) = self.request("DELETE", path, query=query)
        return load(content, metadata=metadata)
