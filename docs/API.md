[← Back to Main README](../README.md)

# CRUD API 

Creating a CRUD (Create, Read, Update, Delete) API with MongoDB and Python for managing user data and online product information. We'll use Flask, a popular lightweight web framework, and PyMongo, the MongoDB driver for Python. Here's a step-by-step guide to get you started:

## API with Native App Install

> :warning: This approach **will only work if the application is runnning natively** in the host. To run this application in a container further steps are required and should visit: [Running your application with containers](DOCKER.md)

### Step 1: Setting Up the Environment

1. **Install MongoDB**: Make sure MongoDB is installed and running on your system. You can download it from the official MongoDB website. (NOTE: It can also be a mongo server running container).

2. **Create a Virtual Environment (Optional but Recommended)**:
   ```bash
   python3 -m venv .venv
   source venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. **Install Required Packages**:
   ```bash
   pip install Flask pymongo docker
   ```

4. If is not running already relaunch `mongodb-server` container

    ```bash
    docker run --rm --name mongodb-server -d -p 27017:27017 mongo
    ```

### Step 2: Initialize Flask App

Create a new Python file (e.g., `app.py`) and set up a basic Flask app.

```python
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
# NOTE! This only work when run natively (on host)
client = MongoClient("mongodb://localhost:27017/")
db = client.test_db  # database name

@app.route('/')
def index():
    return 'Connected to MongoDB version: ' + str(db.command("serverStatus")['version'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
```

### Step 3: Define the CRUD Operations

1. **Create (POST)** - Add a new product or user.
2. **Read (GET)** - Retrieve existing product or user details.
3. **Update (PUT/PATCH)** - Modify an existing product or user.
4. **Delete (DELETE)** - Remove a product or user from the database.

Here's how you can define these operations:

#### Adding a Product/users

Add this to your existent code in `app.py` on your root directory:

```python
# CREATE
@app.route('/products', methods=['POST'])
def add_product():
    product_data = request.get_json()
    result = db.products.insert_one(product_data)
    return jsonify({"message": "Product created successfully", "id": str(result.inserted_id)}), 201


@app.route('/users', methods=['POST'])
def add_user():
    user_data = request.get_json()
    result = db.users.insert_one(user_data)
    return jsonify({"message": "User created successfully", "id": str(result.inserted_id)}), 201

```

#### Retrieving a Product/users

```python
# READ
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = db.products.find_one({"product_id": product_id})
    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product)
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = db.users.find_one({"username": username})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404

```

#### Updating a Product/users

```python
# UPDATE
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    update_data = request.get_json()
    result = db.products.update_one({"product_id": product_id}, {"$set": update_data})

    if result.matched_count:
        return jsonify({"message": "Product updated successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    update_data = request.get_json()
    result = db.users.update_one({"username": username}, {"$set": update_data})

    if result.matched_count:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404
```

#### Deleting a Product/users

```python
# DELETE
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = db.products.delete_one({"product_id": product_id})

    if result.deleted_count:
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404



@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    result = db.users.delete_one({"username": username})

    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404
```

### Step 4: Run the Flask App

Run the Flask app with the command:

```bash
python app.py
```

### Step 5: Test the application

There are several ways of testing this, the most recommended one would be using `Postman` and the `JSON` file under `tests` directory.

- **Postman**
- **Curl**
- **Web Browser**

> For more details on how to test, have a look into [TESTING.md](./TESTING.md)

---

[← Previous: Setup MongoDB for development](./MONGO.md) | [Next: Running your application with containers →](./DOCKER.md)