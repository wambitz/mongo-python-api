from flask import Flask, jsonify, request
from pymongo import MongoClient
from crud import CRUDContext
from user_mongo_crud import UserCRUD  
from product_mongo_crud import ProductCRUD  


app = Flask(__name__)

crud_context = CRUDContext(None)  # Initialize context without a strategy

@app.route('/')
def index():
    return 'Welcome'

# User CRUD operations
@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/users', methods=['GET', 'POST'])
def user(id=None):
    crud_context.set_strategy(UserCRUD())  # Set UserCRUD strategy
    if request.method == 'POST':
        return jsonify(crud_context.create(request.json)), 201
    elif request.method == 'GET':
        return jsonify(crud_context.read(id) if id else crud_context.read()), 200
    elif request.method == 'PUT':
        return jsonify(crud_context.update(id, request.json)), 200
    elif request.method == 'DELETE':
        return jsonify({"message": "User deleted successfully"}) if crud_context.delete(id) else jsonify({"message": "User not found"}), 404

# Product CRUD operations
@app.route('/products/<id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/products', methods=['GET', 'POST'])
def product(id=None):
    crud_context.set_strategy(ProductCRUD())  # Set ProductCRUD strategy
    if request.method == 'POST':
        return jsonify(crud_context.create(request.json)), 201
    elif request.method == 'GET':
        return jsonify(crud_context.read(id) if id else crud_context.read()), 200
    elif request.method == 'PUT':
        return jsonify(crud_context.update(id, request.json)), 200
    elif request.method == 'DELETE':
        return jsonify({"message": "Product deleted successfully"}) if crud_context.delete(id) else jsonify({"message": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
