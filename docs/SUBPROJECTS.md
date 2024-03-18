# HOWTO: Run subprojects

This guide describe different ways of running the subprojects in this repository. Every project builds upon the previous one, each one adds new more complex features:

1. **00_HelloWorld**: Test the connection to Mongo DB.

2. **01_CRUD**: Implements a CRUD API on a single file using Flask and Mongo DB.

3. **02_CRUD_Stragegy**: Implements a CRUD API using the Strategy design pattern and split the implementation in several file and classes.



```bash
cd <path/to/subproject>
```

## Running locally

:exclamation: This can be run locally with `python app.py` if an mongo db server is already running in the host machine and all dependencies are already installed. Is highly suggested to use a virtual environment (`venv`).


## Docker Compose

To tie these containers together, use Docker Compose. Here's a `docker-compose.yml` file to run both services:

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  flask-app:
    build: .
    container_name: flask-app
    ports:
      - "5000:5000"
    networks:
      - app-network
    environment:
      FLASK_APP: app.py
      FLASK_RUN_HOST: 0.0.0.0
      FLASK_ENV: development
    working_dir: /00_HelloWorld
    command: ["flask", "run"]

  mongodb-server:
    image: mongo
    container_name: mongodb-server
    ports:
      - "27017:27017"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

This file defines two services: 
- `web` for your Flask app, building the Dockerfile in the current directory.
- `mongo` for MongoDB, using the official image.

The `depends_on` clause ensures that the `mongo` service is started before the `web` service. The `volumes` directive for MongoDB persists its data across container restarts.

Finally, start both containers with Docker Compose:

```bash
docker-compose -d up
```

Now, your Flask app should be able to communicate with MongoDB. The Flask app is accessible on `localhost:5000`, and it will connect to MongoDB running in another container.

**Tips and Considerations**:

- **Networks**: Docker Compose sets up a default network where services can discover each other by service names (like `mongo` in this case).
- **Security**: For production, consider security aspects. Don’t expose MongoDB port unless necessary, use environment variables for sensitive data, and set up proper authentication.
- **Debugging**: If there are connectivity issues, check the logs and ensure the services are on the same network.
- **MongoDB Configuration**: Depending on your use case, you might want to customize the MongoDB configuration.

Lastily to stop  the containers

```bash
docker-compose down
```

## Scripts

To simplify you execution you can run the following scripts instead of running the arguments manually in the command line

`build.py`:

- Build mongo image
- Build flask app image
- Creates the required docker network to communicate the containers

```python
python build.py
```

`run.py`:

- Run a temporary mongo container in deattached mode
- Run a temporary flask container in deattached mode

```python
python run.py
```

`clean.py`:

Forcefully:

- Removes mongo container
- Removes flask container

```python
python clean.py
```

Notes

- Flask app container cannot communicate with mongo server either locally or in a separate container if the containers are not configured to use the same network

Setting up a Flask app and MongoDB using `docker build` and `docker run` instead of Docker Compose involves a few more manual steps, but it's definitely doable and provides a good understanding of how containers interact. 

## Command line

### 1. **Build the Flask App Docker Image**

First, you need to build a Docker image for your Flask application. Assuming you have the same `Dockerfile` and `app.py` from the previous example, you can build the image like this:

```bash
docker build -t flask-app . -f ../Dockerfile
```

This command builds the Docker image with the tag `flask-app` based on the Dockerfile in the current directory.

### 2. **Network Configuration**

For the Flask app to communicate with MongoDB, both containers need to be on the same network. You can use the default bridge network, but creating a custom network provides better control:

```bash
docker network create app-network
```

If is the mongo container is already running you can connect the MongoDB container to this network:

```bash
docker network connect app-network mongodb-server
```

### 3. **Run the MongoDB Container**

Next, run the MongoDB container. You can pull the official MongoDB image and run it:

```bash
docker run --name mongodb-server --network app-network -d -p 27017:27017 mongo
```

This command runs MongoDB in a container named `mongo`, exposes port 27017 (the default MongoDB port), and runs it in detached mode.



### 4. **Run the Flask App Container**

Now, run your Flask app container and connect it to the same network:

```bash
docker run --rm --name flask-app --network app-network -d -p 5000:5000 flask-app
```

This command runs your Flask app in a container named `flask-app`, exposes port 5000, and connects it to the `app-network`.

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