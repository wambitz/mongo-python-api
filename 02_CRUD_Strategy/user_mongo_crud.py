from crud import CRUDStrategy


class UserCRUD(CRUDStrategy):
    """
    Implements CRUD operations specifically for user documents in a MongoDB collection.

    This class inherits from CRUDStrategy and provides concrete implementations of the
    create, read, update, and delete operations for managing user documents within the
    'users' collection of MongoDB.

    Methods:
        create(data): Inserts a new user document into the collection.
        read(query): Retrieves a user document from the collection based on a query.
        update(query, data): Updates a user document in the collection.
        delete(query): Deletes a user document from the collection.
    """
    def __init__(self):
        """Initializes the UserCRUD class to work with the 'users' collection."""
        super().__init__("users")

    def create(self, data):
        """
        Inserts a new user document into the collection.

        Args:
            data (dict): The user data to insert.

        Returns:
            InsertOneResult: The result object which includes the ID of the newly inserted document.
        """
        return self.collection.insert_one(data)

    def read(self, query):
        """
        Retrieves a user document from the collection based on a query.

        Args:
            query (dict): The query to select the document.

        Returns:
            dict: The first document found matching the query. None if no document matches.
        """
        return self.collection.find_one(query)

    def update(self, query, data):
        """
        Updates a user document in the collection.

        Args:
            query (dict): The query to select the document for update.
            data (dict): The data to update in the selected document.

        Returns:
            UpdateResult: The result object of the update operation.
        """
        return self.collection.update_one(query, {"$set": data})

    def delete(self, query):
        """
        Deletes a user document from the collection.

        Args:
            query (dict): The query to select the document for deletion.

        Returns:
            DeleteResult: The result object of the delete operation.
        """
        return self.collection.delete_one(query)


if __name__ == "__main__":
    # Using the class directly
    user_crud = UserCRUD()

    # Creating a user
    user_id = user_crud.create(
        {"username": "jonhdoe", "name": "John Doe", "email": "john@example.com"}
    ).inserted_id

    # Reading the newly created user
    user = user_crud.read({"_id": user_id})
    print(user)

    # Updating the user's name
    user_crud.update({"_id": user_id}, {"name": "John Dollar"})
    user = user_crud.read({"_id": user_id})
    print(user)

    # Deleting the user
    user_crud.delete({"_id": user_id})
    user = user_crud.read({"_id": user_id})
    print(user)
