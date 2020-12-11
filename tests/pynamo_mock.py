import time
from typing import Any, Optional

from pynamodb.exceptions import TableDoesNotExist


class TableConnectionMock:
    """
    Mockup for pynamodb.table.TableConnection.

    Args:
        table_name (str): The name of the table in PynamoDB.

    Attributes:
        _table_name (str): The name of the table in PynamoDB.
        _data (dict): The data of the DB (instead of a real PyanmoDB).
        _table_metadata (dict): The metadata of the table (initialized in create_table).
    """

    def __init__(self, table_name: str):
        self._table_name = table_name
        self._data = {}
        self._table_metadata = None

    def _get_keys_attributes(self, hash_key: Any, range_key: Any = None):
        """
        Formatting hash key and range key into attributes.

        Args:
            hash_key (Any): The hash key of an item.
            range_key (:obj:`Any`, optional): The range key of an item.
        Returns:
            dict: The keys in PynamoDB's attributes format.s
        """

        keys_attributes = {}
        attributes_definitions = self._table_metadata["AttributeDefinitions"]

        for key in self._table_metadata.get("KeySchema", []):
            attribute_name = key["attribute_name"]
            attribute_type = next(
                attr["attribute_type"]
                for attr in attributes_definitions
                if attribute_name == attr["attribute_name"]
            )
            if key["key_type"] == "HASH":
                keys_attributes[attribute_name] = {attribute_type: hash_key}
            else:
                keys_attributes[attribute_name] = {attribute_type: range_key}

        return keys_attributes

    def put_item(
        self, hash_key: Any, range_key: Optional[Any] = None, attributes: dict = None, **_
    ):
        attributes = attributes or {}
        keys_attributes = self._get_keys_attributes(hash_key, range_key)
        self._data[(hash_key, range_key)] = {**attributes, **keys_attributes}
        return {"ConsumedCapacity": {"TableName": self._table_name, "CapacityUnits": 1.0}}

    def get_item(self, hash_key: Any, range_key: Optional[Any] = None, **_):
        result = {"ConsumedCapacity": {"TableName": self._table_name, "CapacityUnits": 0.5}}
        item = self._data.get((hash_key, range_key))
        return {**result, "Item": item} if item else result

    def scan(self, **_):
        return {
            "Items": list(self._data.values()),
            "Count": len(self._data),
            "ScannedCount": len(self._data),
            "ConsumedCapacity": {"TableName": self._table_name, "CapacityUnits": 0.5},
        }

    def describe_table(self):
        if not self._table_metadata:
            raise TableDoesNotExist(self._table_name)
        return self._table_metadata

    def delete_table(self):
        self._table_metadata = None
        self._data = {}

    def create_table(
        self, attribute_definitions: Optional[Any] = None, key_schema: Optional[Any] = None, **_
    ):
        self._table_metadata = {
            "AttributeDefinitions": attribute_definitions,
            "TableName": self._table_name,
            "KeySchema": key_schema,
            "TableStatus": "ACTIVE",
            "CreationDateTime": time.time(),
            "ItemCount": len(self._data),
        }
