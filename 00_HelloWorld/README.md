# Hello World - Mongo DB Python API with Docker

Creating two containers, one with a small Flask app and another with MongoDB, and ensuring they can communicate with each other is a common task in modern web development. Here's a step-by-step guide on how to achieve this, leveraging Docker. 

## Running locally

:exclamation: This can be run locally with `python app.py` if an mongo db server is already running in the host machine.


## Docker Compose

To tie these containers together, use Docker Compose. Here's a `docker-compose.yml` file to run both services:

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mongo

  mongo:
    image: mongo:latest
    volumes:
      - ./data/db:/data/db
    ports:
      - "27017:27017"
```

This file defines two services: 
- `web` for your Flask app, building the Dockerfile in the current directory.
- `mongo` for MongoDB, using the official image.

The `depends_on` clause ensures that the `mongo` service is started before the `web` service. The `volumes` directive for MongoDB persists its data across container restarts.

### 5. **Run with Docker Compose**

Finally, start both containers with Docker Compose:

```bash
docker-compose up
```

Now, your Flask app should be able to communicate with MongoDB. The Flask app is accessible on `localhost:5000`, and it will connect to MongoDB running in another container.

### Tips and Considerations:

- **Networks**: Docker Compose sets up a default network where services can discover each other by service names (like `mongo` in this case).
- **Security**: For production, consider security aspects. Don’t expose MongoDB port unless necessary, use environment variables for sensitive data, and set up proper authentication.
- **Debugging**: If there are connectivity issues, check the logs and ensure the services are on the same network.
- **MongoDB Configuration**: Depending on your use case, you might want to customize the MongoDB configuration.

## Command line

Setting up a Flask app and MongoDB using `docker build` and `docker run` instead of Docker Compose involves a few more manual steps, but it's definitely doable and provides a good understanding of how containers interact. Let's go through the process:

### 1. **Build the Flask App Docker Image**

First, you need to build a Docker image for your Flask application. Assuming you have the same `Dockerfile` and `app.py` from the previous example, you can build the image like this:

```bash
docker build -t flaskapp .
```

This command builds the Docker image with the tag `flaskapp` based on the Dockerfile in the current directory.

### 2. **Run the MongoDB Container**

Next, run the MongoDB container. You can pull the official MongoDB image and run it:

```bash
docker run --name mongo -d -p 27017:27017 mongo
```

This command runs MongoDB in a container named `mongo`, exposes port 27017 (the default MongoDB port), and runs it in detached mode.

### 3. **Network Configuration**

For the Flask app to communicate with MongoDB, both containers need to be on the same network. You can use the default bridge network, but creating a custom network provides better control:

```bash
docker network create app-network
```

Then, connect the MongoDB container to this network:

```bash
docker network connect app-network mongo
```

### 4. **Run the Flask App Container**

Now, run your Flask app container and connect it to the same network:

```bash
docker run --name flaskapp -d -p 5000:5000 --network app-network flaskapp
```

This command runs your Flask app in a container named `flaskapp`, exposes port 5000, and connects it to the `app-network`.

### 5. **Verify the Setup**

At this point, your Flask application should be running and able to communicate with MongoDB. You can verify by accessing `http://localhost:5000` in your browser or using a tool like `curl`:

```bash
curl http://localhost:5000
```

This should return a message confirming the connection to MongoDB.

### 6. **Debugging**

If you encounter any issues, check the logs of your containers:

```bash
docker logs flaskapp
docker logs mongo
```

### 7. **Cleanup**

When you're done, you can stop and remove the containers:

```bash
docker stop flaskapp mongo
docker rm flaskapp mongo
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