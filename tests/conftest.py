import pytest
from flask import Flask
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute

from flask_pynamodb import PynamoDB

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
def db(app: Flask) -> PynamoDB:
    return PynamoDB(app)


@pytest.fixture
def todo(db: PynamoDB) -> PynamoDB.Model:
    # pylint: disable=missing-class-docstring
    class Todo(db.Model):
        class Meta:
            table_name = "todo"

        todo_id = UnicodeAttribute(hash_key=True)
        name = UnicodeAttribute()
        done = BooleanAttribute()

    Todo.create_table(wait=True)
    yield Todo
    Todo.delete_table()
