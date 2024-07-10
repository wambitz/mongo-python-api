[← Back to Main README](../README.md)

# Running your application with containers

In `app.py` the commented out lines need to be replaced. 

```python

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Replace this:
# client = MongoClient("mongodb://localhost:27017/")
# db = client.amazon_products  # database name

# For this: 
mongodb_host = os.getenv('MONGODB_HOST')
if mongodb_host is None or mongodb_host == '':
    if os.path.exists('/.dockerenv'):
        mongodb_host = 'mongodb-server'
    else:
        mongodb_host = "localhost"

client = MongoClient(f'mongodb://{mongodb_host}:27017/')
db = client.test_db

@app.route('/')
def index():
    return "Welcome to the Amazon Products API!"

# Rest of the CRUD app ...

if __name__ == '__main__':
    app.run(debug=True)

```


## Manual setup

Setting up a Flask app and MongoDB using `docker build` and `docker run` instead of Docker Compose involves a few more manual steps, but it's definitely doable and provides a good understanding of how containers interact. Let's go through the process:

### 1. **Build the Flask App Docker Image**

First, you need to build a Docker image for your Flask application. Assuming you have the same `Dockerfile` and `app.py` from the previous example, you can build the image like this:

```bash
docker build -t flask-app .
```

This command builds the Docker image with the tag `flask-app` based on the Dockerfile in the current directory.

### 2. **Run the MongoDB Container**

Next, run the MongoDB container. You can pull the official MongoDB image and run it:

```bash
docker run --rm --name mongodb-server -d -p 27017:27017 mongo

# Alternatively if the network already exists:
# docker run --rm --name mongodb-server --network app-network -d -p 27017:27017 mongo
```

This command runs MongoDB in a container named `mongo`, exposes port `27017` (the default MongoDB port), and runs it in detached mode.

### 3. **Network Configuration**

For the Flask app to communicate with MongoDB, both containers need to be on the same network. You can use the default bridge network, but creating a custom network provides better control:

```bash
docker network create app-network
```

Verify the network was successfully created:

```bash
docker network ls
```

Then, connect the MongoDB container to this network:

```bash
docker network connect app-network mongodb-server
```

Verify the container is connected to the network:

```bash
docker network inspect app-network
```

### 4. **Run the Flask App Container**

Now, run your Flask app container and connect it to the same network:

```bash
docker run --rm --name flask-app -d -p 5000:5000 --network app-network flask-app
```

Verify the container is the same network

```bash
docker network inspect app-network
```

This command runs your Flask app in a container named `flask-app`, exposes port `5000`, and connects it to the `app-network`.

### 5. **Verify the Setup**

At this point, your Flask application should be running and able to communicate with MongoDB. You can verify by accessing `http://localhost:5000` in your browser or using a tool like `curl`:

```bash
curl http://localhost:5000
```

This should return a message confirming the connection to MongoDB.

### 6. **Debugging**

If you encounter any issues, check the logs of your containers:

```bash
docker logs flask-app
docker logs mongodb-server
```

### 7. **Cleanup**

When you're done, you can stop and remove the containers:

```bash
docker stop flask-app mongodb-server
docker rm flask-app mongodb-server
```

And if you created a custom network, you can remove it too:

```bash
docker network rm app-network
```

### Additional Notes:

- **Data Persistence for MongoDB**: If you need to persist data, you can mount a volume to the MongoDB container.
- **Environment Variables**: You can pass environment variables (like database URL, credentials, etc.) to your Flask app using `-e` flag with `docker run`.
- **Security**: Be cautious with port exposure and security configurations, especially if you're planning for a production deployment.

This approach gives you a more granular control over your containers and helps in understanding the networking and communication between different Docker containers.

---

[← Previous: CRUD API ](./API.md) | [Next: Testing →](./TESTING.md)