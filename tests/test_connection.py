from uuid import uuid4

import pytest
from flask import Flask, request
from flask.testing import Client as FlaskClient
from pynamodb.connection import Connection

from flask_pynamodb import PynamoDB


@pytest.fixture(autouse=True)
def endpoints(app: Flask, db: PynamoDB, todo: PynamoDB.Model):
    # pylint: disable=unused-variable

    table_name = todo.Meta.table_name

    @app.route("/list")
    def index():
        return db.connection.scan(table_name)

    @app.route("/add", methods=["POST"])
    def add():
        if "todo_id" in request.json:
            return 400, "Todo id is auto generated"

        todo_id = str(uuid4())
        return db.connection.put_item(table_name, hash_key=todo_id, attributes=request.json)


def test_invalid_connection(app: Flask, db: PynamoDB):
    with app.app_context():
        app.extensions.pop("pynamodb")
        assert isinstance(db.connection, Connection)


def test_list_todos(client: FlaskClient):
    response = client.get("/list")
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"


def test_add_todo(client: FlaskClient):
    new_todo = {"name": {"S": "test TODO"}, "done": {"BOOL": False}}
    response = client.post("/add", json=new_todo)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
