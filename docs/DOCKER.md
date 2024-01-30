# Running your application with containers

To simplify you execution you cand run the following scripts

`build.py`:

- Build mongo image
- Build flask app image
- Creates the required docker network to communicate the containers

`run.py`:

- Run a temporary mongo container in deattached mode
- Run a temporary flask container in deattached mode

Notes

- Flask app container cannot communicate with mongo server either locally or in a separate container if the containers are not configured to use the same network


## Manual setup

Certainly! Setting up a Flask app and MongoDB using `docker build` and `docker run` instead of Docker Compose involves a few more manual steps, but it's definitely doable and provides a good understanding of how containers interact. Let's go through the process:

### 1. **Build the Flask App Docker Image**

First, you need to build a Docker image for your Flask application. Assuming you have the same `Dockerfile` and `app.py` from the previous example, you can build the image like this:

```bash
docker build -t flaskapp .
```

This command builds the Docker image with the tag `flaskapp` based on the Dockerfile in the current directory.

### 2. **Run the MongoDB Container**

Next, run the MongoDB container. You can pull the official MongoDB image and run it:

```bash
docker run --rm --name mongo-server -d -p 27017:27017 mongo
# Alternatively if the network already exists:
# docker run --rm --name mongo-server --network mongo-network -d -p 27017:27017 mongo
```

This command runs MongoDB in a container named `mongo`, exposes port 27017 (the default MongoDB port), and runs it in detached mode.

### 3. **Network Configuration**

For the Flask app to communicate with MongoDB, both containers need to be on the same network. You can use the default bridge network, but creating a custom network provides better control:

```bash
docker network create mongo-network
```

Then, connect the MongoDB container to this network:

```bash
docker network connect mongo-network mongo-server
```

### 4. **Run the Flask App Container**

Now, run your Flask app container and connect it to the same network:

```bash
docker run --rm --name flaskapp -d -p 5000:5000 --network mongo-network flaskapp
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
docker network rm mongo-network
```

### Additional Notes:

- **Data Persistence for MongoDB**: If you need to persist data, you can mount a volume to the MongoDB container.
- **Environment Variables**: You can pass environment variables (like database URL, credentials, etc.) to your Flask app using `-e` flag with `docker run`.
- **Security**: Be cautious with port exposure and security configurations, especially if you're planning for a production deployment.

This approach gives you a more granular control over your containers and helps in understanding the networking and communication between different Docker containers.