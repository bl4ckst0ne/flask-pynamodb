from uuid import uuid4

import pytest
from flask import Flask, jsonify, request
from flask.testing import Client as FlaskClient

from flask_pynamodb import PynamoDB


@pytest.fixture(autouse=True)
def endpoints(app: Flask, todo: PynamoDB.Model):
    # pylint: disable=unused-variable

    @app.route("/list")
    def index():
        return jsonify([{"todo_id": t.todo_id} for t in todo.scan()])

    @app.route("/add", methods=["POST"])
    def add():
        if "todo_id" in request.json:
            return 400, "Todo id is auto generated"

        new_todo = todo(todo_id=str(uuid4()), **request.json)
        new_todo.save()
        return jsonify({"todo_id": new_todo.todo_id, "name": new_todo.name, "done": new_todo.done})

    @app.route("/get/<todo_id>")
    def get(todo_id: str):
        todo_obj = todo.get_or_404(hash_key=todo_id)
        return jsonify({"todo_id": todo_obj.todo_id, "name": todo_obj.name, "done": todo_obj.done})

    @app.route("/get-advanced/<todo_id>")
    def get_advanced(todo_id: str):
        todo_obj = todo.get_or_404(hash_key=todo_id, message=f"Todo {todo_id} was not found")
        return jsonify({"todo_id": todo_obj.todo_id, "name": todo_obj.name, "done": todo_obj.done})


def test_list_todos(client: FlaskClient):
    response = client.get("/list")
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"


def test_add_todo(client: FlaskClient):
    new_todo = {"name": "test TODO", "done": False}
    response = client.post("/add", json=new_todo)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"


def test_get_todo(client: FlaskClient):
    new_todo = {"name": "test TODO", "done": False}
    response = client.post("/add", json=new_todo)

    assert response.status_code == 200, f"Failed to add todo: status code {response.status_code}"
    assert "todo_id" in response.json, f"Invalid response model: {response.json}"

    todo_id = response.json["todo_id"]
    response = client.get(f"/get/{todo_id}")
    assert response.status_code == 200, f"Failed to get todo: status code {response.status_code}"
    assert response.json.get("todo_id") == todo_id, f"Invalid response model: {response.json}"

    response = client.get(f"/get-advanced/{todo_id}")
    assert response.status_code == 200, f"Failed to get todo: status code {response.status_code}"
    assert response.json.get("todo_id") == todo_id, f"Invalid response model: {response.json}"

    response = client.get("/get/invalid-id")
    assert response.status_code == 404, f"Unexpected status from get todo: {response.status_code}"

    response = client.get("/get-advanced/invalid-id")
    assert response.status_code == 404, f"Unexpected status from get todo: {response.status_code}"
