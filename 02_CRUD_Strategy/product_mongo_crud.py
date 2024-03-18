from crud import CRUDStrategy


class ProductCRUD(CRUDStrategy):
    """
    A CRUD strategy class for product documents in a MongoDB collection.

    This class inherits from CRUDStrategy and implements specific CRUD operations
    for managing product documents in the 'products' collection of MongoDB.

    Methods:
        create(data): Inserts a new product document into the collection.
        read(query): Retrieves a product document from the collection based on a query.
        update(query, data): Updates a product document in the collection.
        delete(query): Deletes a product document from the collection.
    """
    def __init__(self):
        """Initializes the ProductCRUD class for the 'products' collection."""
        super().__init__("products")

    def create(self, data):
        """
        Inserts a new product document into the collection.

        Args:
            data (dict): The product data to insert.

        Returns:
            InsertOneResult: The result object which includes the ID of the newly inserted document.
        """
        return self.collection.insert_one(data)

    def read(self, query):
        """
        Retrieves a product document from the collection based on a query.

        Args:
            query (dict): The query to select the document.

        Returns:
            dict: The first document found matching the query. None if no document matches.
        """
        return self.collection.find_one(query)

    def update(self, query, data):
        """
        Updates a product document in the collection.

        Args:
            query (dict): The query to select the document for update.
            data (dict): The data to update in the selected document.

        Returns:
            UpdateResult: The result object of the update operation.
        """
        return self.collection.update_one(query, {"$set": data})

    def delete(self, query):
        """
        Deletes a product document from the collection.

        Args:
            query (dict): The query to select the document for deletion.

        Returns:
            DeleteResult: The result object of the delete operation.
        """
        return self.collection.delete_one(query)


if __name__ == "__main__":
    # Example usage of the ProductCRUD class
    product_crud = ProductCRUD()

    # Creating a product
    product_id = product_crud.create(
        {"product_id": "123", "name": "Example Product", "price": 29.99}
    )

    # Reading the newly created product
    product = product_crud.read({"_id": product_id})
    print(product)

    # Updating the product's price
    product_crud.update({"_id": product_id}, {"price": 99.99})
    product = product_crud.read({"_id": product_id})
    print(product)

    # Deleting the product
    product_crud.delete({"_id": product_id})
    product = product_crud.read({"_id": product_id})
    print(product)
