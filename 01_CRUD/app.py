import os

from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)

# Initialize MongoDB connection
# Use an environment variable for the MongoDB URI with a default value
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
    return "Connected to MongoDB version: " + str(db.command("serverStatus")["version"])


# CREATE
@app.route("/products", methods=["POST"])
def add_product():
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
    product = db.products.find_one({"product_id": product_id})
    if product:
        product["_id"] = str(product["_id"])
        return jsonify(product)
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
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
    update_data = request.get_json()
    result = db.products.update_one({"product_id": product_id}, {"$set": update_data})

    if result.matched_count:
        return jsonify({"message": "Product updated successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/users/<username>", methods=["PUT"])
def update_user(username):
    update_data = request.get_json()
    result = db.users.update_one({"username": username}, {"$set": update_data})

    if result.matched_count:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


# DELETE
@app.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    result = db.products.delete_one({"product_id": product_id})

    if result.deleted_count:
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    result = db.users.delete_one({"username": username})

    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    # NOTE! host='0.0.0.0' is required to be able to reach the server outside the container
    app.run(host="0.0.0.0", debug=True)
