import pytest
from flask import Flask
from pynamodb.connection.base import Connection

from flask_pynamodb import PynamoDB


def test_invalid_app_at_init():
    with pytest.raises(TypeError) as err:
        PynamoDB("invalid app instance")

    assert str(err.value) == "Invalid Flask app instance."


def test_invalid_app_at_init_app():
    db = PynamoDB()

    with pytest.raises(TypeError) as err:
        db.init_app("Invalid app instance")

    assert str(err.value) == "Invalid Flask app instance."

    with pytest.raises(TypeError) as err:
        db.init_app(None)

    assert str(err.value) == "Invalid Flask app instance."


def test_connection_property(app: Flask, db: PynamoDB):
    with app.app_context():
        assert isinstance(db.connection, Connection)
        assert app.extensions["pynamodb"]["connection"] is db.connection

        app.extensions.pop("pynamodb")
        assert isinstance(db.connection, Connection)


def test_cached_connection(todo: PynamoDB.Model):
    todo._connection = todo._get_connection()
    assert todo._connection is todo._get_connection()
