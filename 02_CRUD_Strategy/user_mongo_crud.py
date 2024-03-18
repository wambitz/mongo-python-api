from crud import CRUDStrategy

class UserCRUD(CRUDStrategy):
    def __init__(self):
        super().__init__('users')

    def create(self, data):
        return self.collection.insert_one(data)

    def read(self, query):
        return self.collection.find_one(query)

    def update(self, query, data):
        return self.collection.update_one(query, {'$set': data})

    def delete(self, query):
        return self.collection.delete_one(query)


if __name__ == '__main__':
    # Using the class directly
    user_crud = UserCRUD()

    user_id = user_crud.create({"username": "jonhdoe", "name": "John Doe", "email": "john@example.com"})
    user = user_crud.read({"_id": user_id})
    print(user)

    user_crud.update({"_id": user_id}, {"name": "John Dollar"})
    user = user_crud.read({"_id": user_id})
    print(user)

    user_crud.delete({"_id": user_id})
    
    user = user_crud.read({"_id": user_id})
    print(user)
