"""Manage data extract or given to HTTPRequest."""
import functools
import json
import re
from abc import ABC, abstractmethod


class Mime:
    """A mime type : https://en.wikipedia.org/wiki/Media_type."""

    def __init__(self, mime_type: str, subtype: str, suffix: str = None, parameters: dict = None):
        """
        Initialize a new mime type.

        :param mime_type: A mime type
        :param subtype: Mime sub type
        :param suffix: Mime suffix
        :param parameters: Mime parameters
        """
        self.type = mime_type
        self.subtype = subtype
        self.suffix = suffix
        self.parameters = parameters

    def __repr__(self) -> str:
        """
        Mime type representation.

        :return: Mime type representation
        """
        message = f"{self.type}/{self.subtype}"
        if self.suffix is not None:
            message += f"+{self.suffix}"
        if self.parameters is not None:
            message += "; ".join([f"{k}={v}" for k, v in sorted(self.parameters.items())])
        return message

    @classmethod
    def parse(cls, mime: str) -> "Mime":
        """
        Parse textual mime and return Mime object.

        :param mime: A textual mime type
        :return: A Mime object
        :raises ValueError: If can't parse mime
        """
        # Parse mime
        m = re.match(r"^(?P<type>[a-z]+)\/(?P<subtype>[a-z-\.]+)(?P<suffix>\+[a-z\.]+)?(; (?P<parameters>.+))?", mime)
        if m is None:
            raise ValueError(f"Can't parse mime type '{mime}'")

        # Split parameter to dict
        parameters = None
        if m.group("parameters"):
            parameters = {}
            for parameter in m.group("parameters").split(";"):
                (k, v) = parameter.split("=")
                parameters[k] = v

        return cls(m.group("type"), m.group("subtype"), suffix=m.group("suffix"), parameters=parameters)


class Serializer(ABC):
    """Convert data from or to python data."""

    @abstractmethod
    def __init__(self, mime: Mime):
        """
        Initialize a new Serializer.

        :param mime: Supported Mime
        """
        self.mime = mime

    @abstractmethod
    def load(self, data):
        """
        Convert to python data.

        :param data: Native data
        :return: Python data
        """
        pass

    @abstractmethod
    def dump(self, data):
        """
        Convert from python data.

        :param data: Python data
        :return: Native data
        """
        pass


class JsonSerializer(Serializer):
    """Serialize json data."""

    def __init__(self):
        super().__init__(Mime("application", "json"))

    def load(self, data):
        return json.loads(data)

    def dump(self, data):
        return json.dumps(data)


class TextSerializer(Serializer):
    """Serialize Text data."""

    def __init__(self):
        super().__init__(Mime("text", "plain"))

    def load(self, data):
        if isinstance(data, bytes):
            return data.decode("utf-8")
        return data

    def dump(self, data):
        return data


class PythonSerializer(Serializer):
    """Serialize python data (mean no-op)."""

    def __init__(self):
        super().__init__(Mime("x-python", "data"))

    def load(self, data):
        if isinstance(data, bytes):
            return data.decode("UTF-8")
        return data

    def dump(self, data):
        return data


class FormURLEncoded(Serializer):
    def __init__(self):
        super().__init__(Mime("application", "x-www-form-urlencoded"))

    def load(self, data):
        if isinstance(data, bytes):
            return data.decode("UTF-8")
        return data

    def dump(self, data):
        return data


@functools.lru_cache(maxsize=None)
def get(name: str) -> Serializer:
    """
    Get a serializer from mime type or subtype.

    :param name: A mime type or subtype name
    :return: Serializer
    :raises TypeError: If data type not supported.
    """
    if name == "json":
        return JsonSerializer()
    if name == "text":
        return TextSerializer()
    if name == "x-python":
        return PythonSerializer()

    raise TypeError(f"Can't find a serializer to process '{name}' type")


def load(data, metadata=None):
    """
    Convert heterogeneous data to python.

    :param data: HTTPRequest data
    :param metadata: HTTPRequest metadata
    :return: Python data
    :raises TypeError: If raw data can't be converted to python
    """
    # If no data, return python serializer
    if data is None:
        return get("x-python").load(data)

    # Extract mime type if available
    if metadata is not None and "Content-Type" in metadata:
        mime = Mime.parse(metadata["Content-Type"])
        # first test subtype
        try:
            serializer = get(mime.subtype)
        except TypeError:
            # then test type
            serializer = get(mime.type)
        return serializer.load(data)

    # If no content, nothing to convert so return python serializer
    if "Content-Length" in metadata and metadata["Content-Length"] == "0":
        return get("x-python").load(data)

    raise TypeError(f"Can't convert data '{data}' with metadata '{metadata}'")
