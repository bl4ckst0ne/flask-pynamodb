import json
from uuid import uuid4

import pytest
from flask import Flask, request
from flask.testing import Client as FlaskClient

from flask_pynamodb import PynamoDB


@pytest.fixture(autouse=True)
def endpoints(app: Flask, todo: PynamoDB.Model):
    # pylint: disable=unused-variable

    @app.route("/list")
    def index():
        return "\n".join(t.name for t in todo.scan())

    @app.route("/add", methods=["POST"])
    def add():
        if "todo_id" in request.json:
            return 400, "Todo id is auto generated"

        new_todo = todo(todo_id=str(uuid4()), **request.json)
        new_todo.save()
        return json.dumps({"name": new_todo.name, "done": new_todo.done})


def test_list_todos(client: FlaskClient):
    response = client.get("/list")
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"


def test_add_todo(client: FlaskClient):
    new_todo = {"name": "test TODO", "done": False}
    response = client.post("/add", json=new_todo)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
