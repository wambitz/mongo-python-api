from flask import Flask
from pymongo import MongoClient

import os


app = Flask(__name__)


# Helper function
def running_in_docker():
    if os.path.exists("/.dockerenv"):
        return True

    return False


@app.route("/")
def hello_world():
    # This will set the mongo host as localhost by default if variable is not set
    # NOTE! localhost won't work with containers, this is setting "mongodb-server" as default,
    # otherwise this can be set by "docker run" + "-e MONGODB_HOST=<mongodb_server_name> ... etc"
    mongodb_host = os.getenv("MONGODB_HOST")
    if mongodb_host is None or mongodb_host == "":
        if running_in_docker():
            mongodb_host = "mongodb-server"
        else:
            mongodb_host = "localhost"

    client = MongoClient(f"mongodb://{mongodb_host}:27017/")
    db = client.test_db
    return "Connected to MongoDB version: " + str(db.command("serverStatus")["version"])
    # return "Hello World"


if __name__ == "__main__":
    # NOTE! host='0.0.0.0' is required to be able to reach the server outside the container
    app.run(debug=True, host="0.0.0.0")
