"""API exceptions."""


class ObjectNotFoundException(Exception):
    """Raised when no api object found."""

    def __init__(self, object_class, **kwargs):
        """
        Initialize a new ObjectNotFoundException.

        :param object_class: API Objet class.
        :param kwargs: lookup param
        """
        super().__init__(f"{object_class.__name__} that match '{kwargs}' not found.")
        self.object_class = object_class
        self.kwargs = kwargs


class NotUniqueObjectException(Exception):
    """Raised when more than one object found."""

    def __init__(self, object_class, pagination, **kwargs):
        """
        Initialize a new NotUniqueObjectException.

        :param object_class: API Objet class.
        :param pagination: A pagination object that contains all items found
        :param kwargs: lookup param
        """
        super().__init__(f"{len(pagination)} {object_class.__name__} that match '{kwargs}' were found.")
        self.object_class = object_class
        self.pagination = pagination
        self.kwargs = kwargs
