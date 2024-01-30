import os

from pymongo import MongoClient
from bson import ObjectId
from crud import CRUDContext, CRUDStrategy


class UserCRUD(CRUDStrategy):
    def __init__(self):
        mongodb_host = os.getenv('MONGODB_HOST', 'localhost')
        self.client = MongoClient(f'mongodb://{mongodb_host}:27017/')  # Set client as an instance attribute
        self.db = self.client['price-tracker']  # Replace 'your_database_name' with the actual name
        self.collection = self.db.users

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
    user_crud = UserCRUD()
    user_id = user_crud.create({"name": "John Doe", "email": "johndoe@example.com"})
    user = user_crud.read(user_id)
    print(user)
    user_crud.update(user_id, {"email": "newemail@example.com"})
    user = user_crud.read(user_id)
    print(user)
    user_crud.delete(user_id)

    # Initialize context with UserCRUD as the default strategy
    crud_context = CRUDContext(UserCRUD())
    # crud_context.set_strategy(UserCRUD())
    user_id = crud_context.create({"name": "John Doe", "email": "johndoe@example.com"})
    user = crud_context.read(user_id)
    print(user)
    crud_context.update(user_id, {"email": "newemail@example.com"})
    user = user_crud.read(user_id)
    print(user)
    crud_context.delete(user_id)
