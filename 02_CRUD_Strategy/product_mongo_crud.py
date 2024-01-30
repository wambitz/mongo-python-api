import os

from pymongo import MongoClient
from bson import ObjectId
from crud import CRUDContext, CRUDStrategy


class ProductCRUD(CRUDStrategy):
    def __init__(self):
        mongodb_host = os.getenv('MONGODB_HOST', 'localhost')
        client = MongoClient(f'mongodb://{mongodb_host}:27017/')
        self.db = self.client.products
        self.collection = self.db.products

    def create(self, data):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def read(self, identifier):
        result = self.collection.find_one({"_id": ObjectId(identifier)})
        if result:
            result['_id'] = str(result['_id'])
        return result

    def update(self, identifier, data):
        result = self.collection.update_one({"_id": ObjectId(identifier)}, {"$set": data})
        return result.matched_count > 0

    def delete(self, identifier):
        result = self.collection.delete_one({"_id": ObjectId(identifier)})
        return result.deleted_count > 0


if __name__ == '__main__':
    # Using the class directly
    product_crud = ProductCRUD()
    product_id = product_crud.create({"product_id": "123", "name": "Example Product", "price": 29.99})
    product = product_crud.read(product_id)
    print(product)
    user_crud.update(product_id, {"price": 99.99})
    user_crud.delete(product_id)

    # Initialize context with UserCRUD as the default strategy
    crud_context = CRUDContext(ProductCRUD())
    # crud_context.set_strategy(ProductCRUD())
    product_id = crud_context.create({"product_id": "123", "name": "Example Product", "price": 29.99})
    product = crud_context.read(product_id)
    print(product)
    crud_context.update(product_id, {"price": 99.99})
    crud_context.delete(product_id)
