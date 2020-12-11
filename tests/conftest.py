from typing import Any, Dict

import pytest
from flask import Flask
from flask.testing import Client as TestClient
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute
from pynamodb.models import Model
from pytest_mock import MockerFixture

from flask_pynamodb import PynamoDB

from .pynamo_mock import TableConnectionMock

# pylint: disable=too-few-public-methods
# pylint: disable=redefined-outer-name


class TestConfig:
    """
    Config class for the testing Flask application.
    """

    DYNAMODB_HOST = "http://localhost:8000"
    DYNAMODB_AWS_ACCESS_KEY_ID = "test"
    DYNAMODB_AWS_SECRET_ACCESS_KEY = "test"
    DYNAMODB_READ_CAPACITY_UNITS = 1
    DYNAMODB_WRITE_CAPACITY_UNITS = 1


@pytest.fixture
def app() -> Flask:
    """
    Testing Flask application.
    """

    flask_app = Flask(__name__)
    flask_app.testing = True
    flask_app.config.from_object(TestConfig)

    return flask_app


@pytest.fixture
def client(app: Flask) -> TestClient:
    return app.test_client()


@pytest.fixture
def db(app: Flask, mocker: MockerFixture) -> PynamoDB:
    """
    DynamoDB manager, with a mocked-up TableConnection.

    Args:
        app (Flask): The testing flask application fixture.
        mocker (MockerFixture): The mocker fixture, for mocking the connection.
    Returns:
        PyanmoDB: The database manager for Flask application.
    """

    connection_mock = TableConnectionMock("todo")

    def get_connection_mock():
        return connection_mock

    mocker.patch.object(Model, "_get_connection", side_effect=get_connection_mock, autospec=True)

    return PynamoDB(app)


@pytest.fixture
def todo(db: PynamoDB) -> PynamoDB.Model:
    """
    Example model for testing PynamoDB.

    Args:
        db (PynamoDB): The DynamoDB manager fixture for the testing.
    Returns:
        PynamoDB.Model: An example model.
    """

    # pylint: disable=missing-class-docstring
    class Todo(db.Model):
        class Meta:
            table_name = "todo"

        todo_id = UnicodeAttribute(hash_key=True)
        name = UnicodeAttribute(range_key=True)
        description = UnicodeAttribute()
        done = BooleanAttribute()

        def serialize(self):
            return {name: getattr(self, name) for name, attr in self.get_attributes().items()}

        @classmethod
        def deserialize(cls, data: Dict[str, Any]):
            return cls._from_data(data)

    Todo.create_table(wait=True)
    yield Todo
    Todo.delete_table()
