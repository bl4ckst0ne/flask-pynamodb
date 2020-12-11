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
        return jsonify([t.serialize() for t in todo.scan()])

    @app.route("/add", methods=["POST"])
    def add():
        if "todo_id" in request.json:
            return 400, "Todo id is auto generated"

        new_todo = todo(todo_id=str(uuid4()), **request.json)
        new_todo.save()
        return jsonify(new_todo.serialize())

    @app.route("/get/<todo_id>")
    def get(todo_id: str):
        name = request.args.get("name")
        if not name:
            return "Missing name", 400

        return jsonify(todo.get_or_404(hash_key=todo_id, range_key=name).serialize())

    @app.route("/get-advanced/<todo_id>")
    def get_advanced(todo_id: str):
        name = request.args.get("name")
        if not name:
            return "Missing name", 400

        todo_obj = todo.get_or_404(
            hash_key=todo_id, range_key=name, message=f"Todo {todo_id} was not found"
        )
        return jsonify(todo_obj.serialize())

    @app.route("/first")
    def first():
        return jsonify(todo.first_or_404().serialize())

    @app.route("/first-advanced")
    def first_advanced():
        return jsonify(todo.first_or_404("There are no TODOs!").serialize())

    @app.route("/clear")
    def clear():
        todo.delete_table()
        todo.create_table(wait=True)
        return "", 200


def test_list_todos(client: FlaskClient):
    response = client.get("/list")
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"


def test_add_todo(client: FlaskClient):
    new_todo = {"name": "TODO1", "done": False, "description": "test TODO"}
    response = client.post("/add", json=new_todo)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"


def test_get_todo(client: FlaskClient):
    new_todo = {"name": "TODO2", "done": False, "description": "test TODO 2"}
    response = client.post("/add", json=new_todo)

    assert response.status_code == 200, f"Failed to add todo: status code {response.status_code}"
    assert "todo_id" in response.json, f"Invalid response model: {response.json}"

    todo_id, todo_name = response.json["todo_id"], response.json["name"]
    response = client.get(f"/get/{todo_id}", query_string={"name": todo_name})
    assert response.status_code == 200, f"Failed to get todo: status code {response.status_code}"
    assert response.json.get("todo_id") == todo_id, f"Invalid response model: {response.json}"

    response = client.get(f"/get-advanced/{todo_id}", query_string={"name": todo_name})
    assert response.status_code == 200, f"Failed to get todo: status code {response.status_code}"
    assert response.json.get("todo_id") == todo_id, f"Invalid response model: {response.json}"

    response = client.get("/get/invalid-id", query_string={"name": "invalid-name"})
    assert response.status_code == 404, f"Unexpected status from get todo: {response.status_code}"

    response = client.get("/get-advanced/invalid-id", query_string={"name": "invalid_name"})
    assert response.status_code == 404, f"Unexpected status from get todo: {response.status_code}"


def test_first_todo(client: FlaskClient):
    new_todo = {"name": "first", "done": False, "description": "test first TODO"}
    response = client.post("/add", json=new_todo)
    assert response.status_code == 200, f"Failed to create todo: {response.status_code}"

    response1 = client.get("/first")
    assert response1.status_code == 200, f"Failed to get todo: {response1.status_code}"
    todo_id1 = response1.json.get("todo_id")
    assert todo_id1, f"Invalid todo model: {response1.json}"

    response2 = client.get("/first-advanced")
    assert response2.status_code == 200, f"Failed to get todo: {response2.status_code}"
    todo_id2 = response2.json.get("todo_id")
    assert todo_id2, f"Invalid todo model: {response2.json}"

    assert todo_id1 == todo_id2, f"Todos are different: {response1.json} {response2.json}"

    response = client.get("/clear")
    assert response.status_code == 200, f"Failed to create database: {response.status_code}"

    response = client.get("/first")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
    response = client.get("/first-advanced")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
