import os
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def hello_world():
    mongodb_host = os.getenv('MONGODB_HOST', 'localhost')
    client = MongoClient(f'mongodb://{mongodb_host}:27017/')
    db = client.test_db
    return 'Connected to MongoDB version: ' + str(db.command("serverStatus")['version'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')