Configuration
==============

Basic Configuration
--------------------

The configuration for DynamoDB is passed via ``Flask.config``.

For example, you can create a configuration object, and use ``Flask.config.from_object`` function:

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


For more information about Flask's configuration, please visit `the Flask documentation <https://flask.palletsprojects.com/en/1.1.x/api/#flask.Config>`_.

The Settings
------------

All settings for the configuration has the prefix *DYANMODB*:

**DYNAMODB_REGION**

The default AWS region to connect to. The default region is us-east-1.

**DYNAMODB_HOST**

The address of DyanmoDB, in case of a local DynamoDB.
For more information, please visit PynamoDB's documentation about `Using PynamoDB locally <https://pynamodb.readthedocs.io/en/latest/local.html?highlight=host>`_.

**DYNAMODB_CONNECT_TIMEOUT_SECONDS**

The time in seconds till a ``ConnectTimeoutError`` is thrown when attempting to make a connection.
The default value is 15 seconds.

**DYNAMODB_READ_TIMEOUT_SECONDS**

The time in seconds till a ``ReadTimeoutError`` is thrown when attempting to read from a connection.
The default value is 30 seconds.

**DYNAMODB_BASE_BACKOFF_MS**

The base number of milliseconds used for exponential backoff and jitter on retries.
The default value is 25 milliseconds.

**DYNAMODB_MAX_RETRY_ATTEMPTS**

The number of times to retry certain failed DynamoDB API calls.
The most common cases eligible for retries include ``ProvisionedThroughputExceededException`` and ``5xx`` errors.
The default value is 3 retries.

**DYNAMODB_MAX_POOL_CONNECTIONS**

The maximum number of connections to keep in a connection pool.
The default value is 10 connections.

**DYNAMODB_EXTRA_HEADERS**

A dictionary of headers that should be added to every request.
This is only useful when interfacing with DynamoDB through a proxy, where headers are stripped by the proxy before forwarding along.
Failure to strip these headers before sending to AWS will result in an ``InvalidSignatureException`` due to request signing.

**DYNAMODB_READ_CAPACITY_UNITS**
**DYNAMODB_WRITE_CAPACITY_UNITS**

The default read and write capacity units for DynamoDB's tables.

**DYNAMODB_AWS_ACCESS_KEY_ID**
**DYNAMODB_AWS_SECRET_ACCESS_KEY**
**DYNAMODB_AWS_SESSION_TOKEN**

The credentials for authenticating against DynamoDB.
For more information, please visit PynamoDB's docs about `AWS Access <https://pynamodb.readthedocs.io/en/latest/awsaccess.html>`_.
