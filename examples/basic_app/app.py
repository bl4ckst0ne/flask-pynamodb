from uuid import uuid4

from flask import Flask, render_template
from flask_pynamodb import PynamoDB
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute

from config import Config

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


def create_todos():
    for i in range(10):
        todo = Todo(str(uuid4()), name=f"Todo {i}", description="My TODO!", done=i % 2)
        todo.save()


@app.route("/")
def index():
    return render_template("index.html", todos=list(Todo.scan()))


if __name__ == "__main__":
    Todo.create_table(wait=True)
    create_todos()
    app.run(debug=True)
