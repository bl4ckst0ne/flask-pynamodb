The Model API
===============

Defining a Model
-----------------

A ``Model`` describes a single table inside DynamoDB. Its instances describe records from this table.
As mentioned in PynamoDB's documentation, The most powerful feature of PynamoDB is the ``Model`` API.

You start using it by defining a model class that inherits from ``flask_pynamo.PynamoDB.Model``.
Then, you add attributes to the model that inherit from ``pynamodb.attributes.Attribute``.

.. code-block:: python

    from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

    class Todo(db.Model):
        class Meta:
            table_name = "todo"

        id = UnicodeAttribute(hash_key=True)
        name = UnicodeAttribute()
        description = UnicodeAttribute()
        done = BooleanAttribute(defult=False)


All DynamoDB tables have a hash key, and you must specify which attribute is the hash key for each ``Model`` you define.


Creating New Items
------------------

For creating the table, use ``Model.create_table`` class method. In our case, we should use ``Todo.create_table``.

To create a new record in the table, create a new instance, and call to the ``save`` method.
The first two positional arguments are the ``hash_key`` and the ``range_key``.

.. code-block:: python

    from uuid import uuid4

    todo = Todo(str(uuid4()), name="my todo", description="my first todo!")
    todo.save()


Getting Existing Items
-----------------------

To retrieve an existing item in your table, you can do that with ``get``.
If the item does not exist, ``Todo.DoesNotExist`` will be raised.

.. code-block:: python

    todo = Todo.get('my_todo_id')

You can also use ``get_or_404``, so if the item does not exist the function will call to ``abort(404)``.

In addition, you can use ``first_or_404`` to get the first item from the table.
If the table is empty, it function will call to ``abort(404)``.
