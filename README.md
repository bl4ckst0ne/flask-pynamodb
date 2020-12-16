# Flask-PynamoDB

[![codecov](https://codecov.io/gh/bl4ckst0ne/flask-pynamodb/branch/main/graph/badge.svg)](https://codecov.io/gh/bl4ckst0ne/flask-pynamodb)


Flask-PynamoDB is an externsion for [Flask](https://flask.palletsprojects.com/en/1.1.x/) that integrates with [DynamoDB](https://aws.amazon.com/dynamodb/) using the powerful [PynamoDB](https://pynamodb.readthedocs.io/en/latest/) library.

Flask-PynamoDB simplfies the configuration of PynamoDB for your application, as well as adds utilities for better integration with PynamoDB.

## Installation

You can install & update the library using [pip](https://pip.pypa.io/en/stable/):

```python
python -m pip install -U Flask-PynamoDB
```

or:

```python
pip install -U Flask-PynamoDB
```

## Quickstart

```python
from uuid import uuid4
from typing import List

from flask import Flask, render_template
from flask_pynamodb import PynamoDB
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute


class Config:
    DYNAMODB_HOST = "http://localhost:8000"
    DYNAMODB_AWS_ACCESS_KEY_ID = "test"
    DYNAMODB_AWS_SECRET_ACCESS_KEY = "test"
    DYNAMODB_READ_CAPACITY_UNITS = 10
    DYNAMODB_WRITE_CAPACITY_UNITS = 10


app = Flask(__name__)
app.config.from_object(Config)
db = PynamoDB(app)


class Todo(db.Model):
    class Meta:
        table_name = "todo"

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    done = BooleanAttribute(default=False)


@app.route("/")
def index() -> List[str]:
    return [todo.name for i in Todo.scan()]

```