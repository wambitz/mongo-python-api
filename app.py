from flask import Flask, jsonify, request
from pymongo import MongoClient

import os

app = Flask(__name__)

mongodb_host = os.getenv("MONGODB_HOST")
if mongodb_host is None or mongodb_host == "":
    if os.path.exists("/.dockerenv"):
        mongodb_host = "mongodb-server"
    else:
        mongodb_host = "localhost"

client = MongoClient(f"mongodb://{mongodb_host}:27017/")
db = client.test_db


@app.route("/")
def index():
    """Root endpoint that provides MongoDB server version.

    Returns:
        str: A message indicating connection to MongoDB with its version.
    """
    return "Connected to MongoDB version: " + str(db.command("serverStatus")["version"])


# CREATE
@app.route("/products", methods=["POST"])
def add_product():
    """Creates a new product in the database.

    The product data is expected in JSON format in the request body.

    Returns:
        tuple: JSON response with the creation message and the new product ID, along with the HTTP status code 201.
    """
    product_data = request.get_json()
    result = db.products.insert_one(product_data)
    return (
        jsonify(
            {"message": "Product created successfully", "id": str(result.inserted_id)}
        ),
        201,
    )


@app.route("/users", methods=["POST"])
def add_user():
    """Creates a new user in the database.

    The user data is expected in JSON format in the request body.

    Returns:
        tuple: JSON response with the creation message and the new user ID, along with the HTTP status code 201.
    """
    user_data = request.get_json()
    result = db.users.insert_one(user_data)
    return (
        jsonify(
            {"message": "User created successfully", "id": str(result.inserted_id)}
        ),
        201,
    )


# READ
@app.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    """Fetches a single product from the database by its product_id.

    Args:
        product_id (str): The ID of the product to retrieve.

    Returns:
        tuple: JSON response with the product data if found, along with the HTTP status code. 404 if not found.
    """
    product = db.products.find_one({"product_id": product_id})
    if product:
        product["_id"] = str(product["_id"])
        return jsonify(product)
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    """Fetches a single user from the database by username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        tuple: JSON response with the user data if found, along with the HTTP status code. 404 if not found.
    """
    user = db.users.find_one({"username": username})
    if user:
        user["_id"] = str(
            user["_id"]
        )  # Convert ObjectId to string for JSON serialization
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404


# UPDATE
@app.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    """Updates a product in the database identified by its product_id.

    Args:
        product_id (str): The ID of the product to update.

    Returns:
        tuple: JSON response with an update success message, along with the HTTP status code. 404 if not found.
    """
    update_data = request.get_json()
    result = db.products.update_one({"product_id": product_id}, {"$set": update_data})

    if result.matched_count:
        return jsonify({"message": "Product updated successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/users/<username>", methods=["PUT"])
def update_user(username):
    """Updates a user in the database identified by username.

    Args:
        username (str): The username of the user to update.

    Returns:
        tuple: JSON response with an update success message, along with the HTTP status code. 404 if not found.
    """
    update_data = request.get_json()
    result = db.users.update_one({"username": username}, {"$set": update_data})

    if result.matched_count:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


# DELETE
@app.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Deletes a product from the database by its product_id.

    Args:
        product_id (str): The ID of the product to delete.

    Returns:
        tuple: JSON response with a deletion success message, along with the HTTP status code. 404 if not found.
    """
    result = db.products.delete_one({"product_id": product_id})

    if result.deleted_count:
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    """Deletes a user from the database by username.

    Args:
        username (str): The username of the user to delete.

    Returns:
        tuple: JSON response with a deletion success message, along with the HTTP status code. 404 if not found.
    """
    result = db.users.delete_one({"username": username})

    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    # NOTE! host='0.0.0.0' is required to be able to reach the server outside the container
    app.run(host="0.0.0.0", debug=True)
