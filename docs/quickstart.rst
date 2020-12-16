Quickstart
===========

PynamoDB is a Pythonic interface to AWS DynamoDB.
Flask-PynamoDB provides integration with PynamoDB to support this Pythonic interface inside Flask.

Installation
-------------

You can easily install Flask-PynamoDB with **pip**:

.. code-block:: sh

    pip install flask-pynamodb

or:

.. code-block:: sh

    python -m pip install flask-pynamodb


Don't have pip? `Follow these instructions for installing pip <https://pip.pypa.io/en/latest/installing/>`_.


A Basic Application
--------------------

To connect your Flask application with DynamoDB, all you have to do is add a configuration
to your application, and create the ``PynamoDB`` object.

.. code-block:: python

    from flask import Flask
    from flask_pynamodb import PynamoDB

    class Config:
        DYNAMODB_HOST = "http://localhost:8000"
        DYNAMODB_AWS_ACCESS_KEY_ID = "test"
        DYNAMODB_AWS_SECRET_ACCESS_KEY = "test"
        DYNAMODB_READ_CAPACITY_UNITS = 1
        DYNAMODB_WRITE_CAPACITY_UNITS = 1

    app = Flask(__name__)
    app.config.from_object(Config)
    db = PynamoDB(app)


Declaring models is the same as in *PynamoDB*, but the base model class is ``flask_pynamo.PynamoDB.Model``.
Notice that you should import the attributes from `pynamodb`.

.. code-block:: python

    from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

    class Todo(db.Model):
        class Meta:
            table_name = "todo"

        id = UnicodeAttribute(hash_key=True)
        name = UnicodeAttribute()
        description = UnicodeAttribute()
        done = BooleanAttribute(defult=False)


Now, we can use the regular functions from *PynamoDB*, such as ``get``, ``scan``, ``save``, etc.
However, we can use the new helper functions for Flask:

- ``get_or_404``: Tries to get a record from the table. If not found, the function raises a 404 error.
- ``first_or_404``: Tries to get the first record from the table. If the table is empty, the function raises a 404 error.

.. code-block:: python

    from typing import List

    @app.route("/todo")
    def list_todos() -> List[str]:
        return [t.name for t in Todo.scan()]

    @app.route("/todo/<todo_id>")
    def get_todo(todo_id: str) -> Todo:
        return Todo.get_or_404(todo_id)