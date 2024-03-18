#!/usr/bin/env python3

from pymongo import MongoClient
from pymongo.collection import Collection

import os


class CRUDStrategy:
    """
    A CRUD strategy class for MongoDB collection operations.

    This class provides a template for create, read, update, and delete operations on a specified MongoDB
    collection. It establishes a connection to MongoDB upon initialization and selects the specified
    collection for performing operations. The class methods are intended to be overridden by subclasses
    implementing specific CRUD operations.

    Attributes:
        collection (Collection): The MongoDB collection object for CRUD operations.
    """
    _mongodb_host = os.getenv("MONGODB_HOST")
    if _mongodb_host is None or _mongodb_host == "":
        if os.path.exists("/.dockerenv"):
            _mongodb_host = "mongodb-server"
        else:
            _mongodb_host = "localhost"
    _client = MongoClient(f"mongodb://{_mongodb_host}:27017/")
    _db = _client["test_db"]

    def __init__(self, collection_name: str):
        """
        Initializes the CRUDStrategy class with the specified MongoDB collection.

        Args:
            collection_name (str): The name of the collection to perform operations on.
        """
        self.collection: Collection = self._db[collection_name]

    def create(self, data):
        """Creates a document in the collection. Should be implemented by subclasses."""
        raise NotImplementedError("Create method not implemented")

    def read(self, query):
        """Reads documents from the collection based on a query. Should be implemented by subclasses."""
        raise NotImplementedError("Read method not implemented")

    def update(self, query, data):
        """Updates documents in the collection based on a query. Should be implemented by subclasses."""
        raise NotImplementedError("Update method not implemented")

    def delete(self, query):
        """Deletes documents from the collection based on a query. Should be implemented by subclasses."""
        raise NotImplementedError("Delete method not implemented")

    def version(self):
        """
        Returns the version of the MongoDB server.

        Returns:
            str: A string containing the MongoDB server version.
        """
        return "Connected to MongoDB version: " + str(
            _db.command("serverStatus")["version"]
        )


if __name__ == "__main__":
    # Example usage of the CRUDStrategy class
    crud = CRUDStrategy("test")
    test_id = None


    # Example CRUD operations
    try:
        test_id = crud.create(
            {"product_id": "123", "name": "Example Product", "price": 29.99}
        )
    except Exception as e:
        print(f"{e}")

    try:
        test_id = crud.read({"_id": test_id})
    except Exception as e:
        print(f"{e}")

    try:
        crud.update({"_id": test_id}, {"price": 99.99})
    except Exception as e:
        print(f"{e}")

    try:
        crud.delete({"_id": test_id})
    except Exception as e:
        print(f"{e}")
