from typing import Any, Dict

from flask import abort
from pynamodb.connection.table import TableConnection
from pynamodb.models import Model as PynamoModel


class Model(PynamoModel):
    """
    The base model, with the application's config.
    The model is backed by a table inside DynamoDB.
    """

    _app_config: Dict[str, Any] = {}

    @classmethod
    def get_or_404(cls, *args, **kwargs) -> "Model":
        """
        Gets an item and raises a 404 Not Found error if the item does not exist.

        Args:
            hash_key (str): The hash key of the desired item.
            range_key (:obj:`str`, optional): The range key of the desired item,
                only used when appropriate.
            consistent_read (bool):
            attributes_to_get (:obj:`Sequence`, optional):
            message: Custom message for the 404 Not Found error.
        Returns:
            Model: An instance of the model for the desired item.
        Raises:
            HTTPException: if the item does not exist, 404 Not Found error will be raised.
        """

        message = kwargs.pop("message", "")

        try:
            return cls.get(*args, **kwargs)
        except cls.DoesNotExist:
            if message:
                abort(404, message)
            abort(404)

    @classmethod
    def first_or_404(cls, message: str = "") -> "Model":
        """
        Gets the first item from the table.

        Args:
            message (str): Custom message for the 404 Not Found error.
        Returns:
            Model: An instance of the model for the desired item.
        Raises:
            HTTPException: if the item does not exist, 404 Not Found error will be raised.
        """

        try:
            return next(cls.scan(page_size=1))
        except StopIteration:
            if message:
                abort(404, message)
            abort(404)

    @classmethod
    def _get_connection(cls) -> TableConnection:
        """
        Gets a (cached) connection to the database, with the application's config.

        Returns:
            TableConnection: The connection to the database.
        """

        meta = getattr(cls, "Meta", None)

        if not meta or cls._connection:
            return super()._get_connection()

        for key, value in cls._app_config.items():
            if not getattr(meta, key, None):
                setattr(meta, key, value)

        return super()._get_connection()
