from typing import Any, Dict

from flask import Flask, current_app
from pynamodb.connection import Connection

from flask_pynamodb.model import Model as ModelClass

__version__ = "0.0.1"


DYNAMODB_SETTINGS = (
    "DYNAMODB_REGION",
    "DYNAMODB_HOST",
    "DYNAMODB_CONNECT_TIMEOUT_SECONDS",
    "DYNAMODB_READ_TIMEOUT_SECONDS",
    "DYNAMODB_BASE_BACKOFF_MS",
    "DYNAMODB_MAX_RETRY_ATTEMPTS",
    "DYNAMODB_MAX_POOL_CONNECTIONS",
    "DYNAMODB_EXTRA_HEADERS",
    "DYNAMODB_AWS_ACCESS_KEY_ID",
    "DYNAMODB_AWS_SECRET_ACCESS_KEY",
    "DYNAMODB_AWS_SESSION_TOKEN",
    "DYNAMODB_READ_CAPACITY_UNITS",
    "DYNAMODB_WRITE_CAPACITY_UNITS",
)


class PynamoDB:
    """
    The main class for initializing and managing PynamoDB integration to one / multiple
    Flask applications.

    Attributes:
        app (Flask): The Flask application that uses DynamoDB. For using more that one app,
            you should use ``init_app`` method. Please note the model class supports a configuration
            of one app only.
    """

    Model = ModelClass

    def __init__(self, app: Flask = None):
        self.app = app

        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        Initializes a Flask application for using the integration.
        Currently, the model class supports a single app configuration only.
        Therefore, if there are multiple app configurations for this integration,
            the configuration will be overriden.

        Args:
            app (Flask): The flask application to initialize.
        """

        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask app instance.")

        self.Model._app_config.update(
            {self._convert_key(k): v for k, v in app.config.items() if k in DYNAMODB_SETTINGS}
        )

        connection = self._create_connection(self.Model._app_config)
        app.extensions["pynamodb"] = {"db": self, "connection": connection}

    @property
    def connection(self) -> Connection:
        """
        str: Base connection object, for accessing DynamoDB.
        """

        try:
            return current_app.extensions["pynamodb"]["connection"]
        except KeyError:
            new_connection = self._create_connection(self.Model._app_config)
            current_app.extensions["pynamodb"] = {
                "db": self,
                "connection": new_connection,
            }
            return new_connection

    @staticmethod
    def _convert_key(key: str) -> str:
        return key.split("_", 1)[1].lower()

    @staticmethod
    def _create_connection(config: Dict[str, Any]) -> Connection:
        connection = Connection(
            config.get("region"),
            config.get("host"),
            config.get("connect_timeout_seconds"),
            config.get("read_timeout_seconds"),
            config.get("max_retry_attempts"),
            config.get("base_backoff_ms"),
            config.get("max_pool_connections"),
            config.get("extra_headers"),
        )

        connection.session.set_credentials(
            config.get("aws_access_key_id"), config.get("aws_secret_access_key")
        )

        return connection
