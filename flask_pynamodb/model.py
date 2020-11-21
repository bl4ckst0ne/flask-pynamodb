from typing import Any, Dict

from pynamodb.connection.table import TableConnection
from pynamodb.models import Model as PynamoModel


class Model(PynamoModel):
    """
    The base model, with the application's config.
    The model is backed by a table inside DynamoDB.
    """

    _app_config: Dict[str, Any] = {}

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
