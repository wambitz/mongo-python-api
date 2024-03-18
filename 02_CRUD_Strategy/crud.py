#!/usr/bin/env python3

from pymongo import MongoClient
from pymongo.collection import Collection

import os

class CRUDStrategy:
    _mongodb_host = os.getenv('MONGODB_HOST')
    if _mongodb_host is None or _mongodb_host == '':
        if os.path.exists('/.dockerenv'):
            _mongodb_host = 'mongodb-server'
        else:
            _mongodb_host = "localhost"
    _client = MongoClient(f'mongodb://{_mongodb_host}:27017/')
    _db = _client['test_db']

    def __init__(self, collection_name: str):
        self.collection: Collection = self._db[collection_name]

    def create(self, data):
        raise NotImplementedError("Create method not implemented")

    def read(self, query):
        raise NotImplementedError("Read method not implemented")

    def update(self, query, data):
        raise NotImplementedError("Update method not implemented")

    def delete(self, query):
        raise NotImplementedError("Delete method not implemented")
    
    def version(self):
        return 'Connected to MongoDB version: ' + str(_db.command("serverStatus")['version'])


if __name__ == '__main__':
    # Using the class directly
    crud = CRUDStrategy("test")
    test_id = None

    try:
        test_id = crud.create({"product_id": "123", "name": "Example Product", "price": 29.99})
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
    



