from flask import Flask, jsonify, request
from user_mongo_crud import UserCRUD
from product_mongo_crud import ProductCRUD


app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome!"


# User CRUD operations
@app.route("/users/<username>", methods=["GET", "PUT", "DELETE"])
@app.route("/users", methods=["GET", "POST"])
def user(username=None):

    users = UserCRUD()

    if request.method == "POST":
        user_data = request.get_json()
        result = users.create(user_data)
        return (
            jsonify(
                {"message": "User created successfully", "id": str(result.inserted_id)}
            ),
            201,
        )

    elif request.method == "GET":
        user = users.read({"username": username})
        if user:
            user["_id"] = str(user["_id"])
            return jsonify(user)
        else:
            return jsonify({"message": "User not found"}), 404

    elif request.method == "PUT":
        update_data = request.get_json()
        result = users.update({"username": username}, update_data)
        if result.matched_count:
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    elif request.method == "DELETE":
        result = users.delete({"username": username})
        if result.deleted_count:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404


# Product CRUD operations
@app.route("/products/<product_id>", methods=["GET", "PUT", "DELETE"])
@app.route("/products", methods=["GET", "POST"])
def product(product_id=None):

    products = ProductCRUD()

    if request.method == "POST":
        product_data = request.get_json()
        result = products.create(product_data)
        return (
            jsonify(
                {
                    "message": "Product created successfully",
                    "id": str(result.inserted_id),
                }
            ),
            201,
        )

    elif request.method == "GET":
        product = products.read({"product_id": product_id})
        if product:
            product["_id"] = str(product["_id"])
            return jsonify(product)
        else:
            return jsonify({"message": "Product not found"}), 404

    elif request.method == "PUT":
        update_data = request.get_json()
        result = products.update({"product_id": product_id}, update_data)
        if result.matched_count:
            return jsonify({"message": "Product updated successfully"}), 200
        else:
            return jsonify({"message": "Product not found"}), 404

    elif request.method == "DELETE":
        result = products.delete({"product_id": product_id})
        if result.deleted_count:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    # NOTE! host='0.0.0.0' is required to be able to reach the server outside the container
    app.run(host="0.0.0.0", debug=True)
