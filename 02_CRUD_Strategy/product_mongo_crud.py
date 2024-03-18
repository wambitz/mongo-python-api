from crud import CRUDStrategy

class ProductCRUD(CRUDStrategy):
    def __init__(self):
        super().__init__('products')

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
    product_crud = ProductCRUD()

    product_id = product_crud.create({"product_id": "123", "name": "Example Product", "price": 29.99})
    product = product_crud.read({"_id": product_id})
    print(product)

    product_crud.update({"_id": product_id}, {"price": 99.99})
    product = product_crud.read({"_id": product_id})
    print(product)

    product_crud.delete({"_id": product_id})
    
    product = product_crud.read({"_id": product_id})
    print(product)
