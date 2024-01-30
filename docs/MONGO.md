# MongoDB Notes

## Installing Mongo Locally on Windows

Installing Mongo Server and Client locally on Windows involves a series of steps:

### 1. Download MongoDB and MongoSH Community Server

1. **Visit the MongoDB Download Center**: Go to the [MongoDB Download Center](https://www.mongodb.com/try/download/community) and [MongoSH Download Center](https://www.mongodb.com/try/download/shell)

2. **Select the Version**: Choose the latest version or the one that suits your requirements.

3. **Choose Your Platform**: Select "Windows".

4. **Choose Package Type**: Select the ZIP package.

5. **Download**: Click the "Download" button to get the installer.

### 2. Install MongoDB

1. **Unzip the binaries**: Once the download is complete, extract your the content on your installation directory. E.g. `C:\Tools\Mongo`

2. **Set Data Directory***: MongoDB needs a directory to store its data. The default path is `C:\data\db\`. You can choose a different path if necessary, but ensure MongoDB has read and write permissions to that directory.

### 3. Set Up Environment Variable

1. **Add MongoDB Path to Environment Variables**: To use MongoDB from the command line, you need to add the MongoDB server's binary file path to your system's PATH environment variable.
   
2. **Locate the Bin Directory**: The `bin` directory is usually located in `C:\InstallDir\MongoDB\Server\{version}\bin` and `C:\InstallDir\MongoDB\Shell\{version}\bin`. Replace `{version}` with your installed version. 

3. **Edit System Environment Variables**:
   - Right-click on “This PC” or “My Computer” on your desktop or in File Explorer.
   - Click “Properties”.
   - Click “Advanced system settings”.
   - In the “System Properties” window, click the “Environment Variables” button.
   - In the “System Variables” section, scroll down and select the “Path” variable, then click “Edit”.
   - Click “New” and add the path to the MongoDB and MongoSH `bin` directory.
   - Click “OK” to close all dialog boxes.

### 4. Verify Installation

1. **Open Command Prompt**: Open a command prompt window.

2. **Run MongoDB Version Check**: Type `mongod --version` and `mongosh --version` to check if MongoDB was installed correctly. This should display the version of MongoDB that's been installed.

### 5. Starting MongoDB

1. **Create Data Directory**: If you didn't set a custom data directory during installation, create the default directory. Run `mkdir C:\data\db` in the command prompt.

2. **Start MongoDB**: Run `mongod` in the command prompt. This starts the MongoDB server.

3. **Access MongoDB Shell**: Open another command prompt and type `mongo`. This opens the MongoDB shell connected to your local MongoDB server.

## Testing Mongo Locally

To interact with your MongoDB instance, you can use the MongoDB shell, `mongosh`, which is a command-line client for MongoDB. It allows you to query and update data as well as perform administrative operations.

Here's how you can open the MongoDB shell:

1. **Open Command Prompt**: Open a new Command Prompt window or PowerShell window.

2. **Start the MongoDB Shell**: Simply type `mongosh` and press Enter. This command connects to your local MongoDB instance.

   ```bash
   mongosh
   ```

   By default, `mongosh` attempts to connect to a MongoDB server running on the localhost (127.0.0.1) and the default port (27017). If your MongoDB server is running with different settings, you can specify them in the command, for example:

   ```bash
   mongosh --host <hostname or IP> --port <port number>
   ```

3. **Using the MongoDB Shell**: Once in the shell, you can start issuing commands to interact with your MongoDB databases. Here are a few basic commands to get you started:

   - Show all databases:
     ```mongodb
     show dbs
     ```
   - Use a specific database (it will create a new one if it doesn't exist):
     ```mongodb
     use <database_name>
     ```
   - Show all collections in the current database:
     ```mongodb
     show collections
     ```
   - Basic query on a collection:
     ```mongodb
     db.<collection_name>.find()
     ```

4. **Exiting the MongoDB Shell**: To exit the shell, you can simply type `exit` and press Enter.

   ```bash
   exit
   ```

The MongoDB shell (`mongo`) is a powerful tool for interacting with your MongoDB database. It supports a wide range of operations from simple queries to complex aggregations. As you're already experienced in software engineering, you'll find the MongoDB shell's syntax straightforward, especially if you're familiar with JSON-like structures.

Remember, MongoDB uses JavaScript-like syntax for its shell commands, which can be very convenient for running quick queries or administrative tasks. You might also want to explore GUI tools like MongoDB Compass for a more visual approach to managing your MongoDB databases, especially for more complex queries and data visualization.




## Installing Mongo on in a Docker container

Using MongoDB in a Docker container is a great way to set up a flexible and isolated development environment. 

### Step 1: Pull the MongoDB Docker Image

First, you need to pull the official MongoDB image from Docker Hub. Open your command line and run:

```bash
docker pull mongo
```

This command downloads the latest official MongoDB image to your local machine.

### Step 2: Run MongoDB in a Docker Container

**Temporary Container**: To test MongoDB inside a temporary container, use the following command:

```bash
docker run --rm -d -p 27017:27017 mongo
```

Explanation of the parameters:
- `--rm`: Creates a temporary container that gets destroyed on exit.
- `-d`: Runs the container in detached mode (in the background).
- `-p 27017:27017`: Maps the default MongoDB port (27017) from the container to the host machine.

**Persistent Container**: To run MongoDB inside a persistent container, use the following command:

```bash
docker run --name mongodb -d -p 27017:27017 mongo
```

Explanation of the parameters:
- `--name mongodb`: Names the container "mongodb".
- `-d`: Runs the container in detached mode (in the background).
- `-p 27017:27017`: Maps the default MongoDB port (27017) from the container to the host machine.

### Step 3: Verify the Container is Running

Check if the MongoDB container is running with:

```bash
docker ps
```

### Step 4: Interacting with MongoDB

Now, MongoDB is running in a Docker container. You can interact with it just like a regular MongoDB instance.


1. **Host: Connect using `mongosh`**: If you have `mongosh` installed on your host machine, you can connect to the MongoDB instance running inside the container:

   ```bash
   mongosh --host localhost --port 27017
   ```

2. **Container: Connect using Docker Exec**: You can also connect to the MongoDB shell directly within the container:

   **Temporary Container**:
   ```bash
   docker exec -it <contained_id> mongosh
   ```

   **Persistent Container**
   ```bash
   docker exec -it mongodb mongosh
   ```

### Step 5: Managing the MongoDB Container

#### **Temporary Container**:

**Server**: To exit the server just do `Ctrl + C` in the terminal instance where `mongod` is running if is a non-deattached session. For a deattached session find the `<container_id>` with `docker ps` :

```
docker stop <container_id>
```

**Client**: To exit the shell prompt type:

```
exit
``` 

#### **Consistent Container**:

- **Stopping the Container**: When you're done, you can stop the container:

  ```bash
  docker stop mongodb
  ```

- **Starting the Container Again**: To start it again:

  ```bash
  docker start mongodb
  ```

- **Accessing Logs**: To see the logs of the MongoDB container:

  ```bash
  docker logs mongodb
  ```

- **Removing the Container**: If you want to remove the container:

  ```bash
  docker rm -f mongodb
  ```

### Data Persistence

One important aspect of running MongoDB in Docker is data persistence. Without proper configuration, data stored in the MongoDB container will be lost when the container is removed.

To persist data, you can mount a directory from your host machine to the container:

```bash
docker run --name mongodb -d -p 27017:27017 -v /my/own/datadir:/data/db mongo
```

Replace `/my/own/datadir` with the path to a directory on your host machine. This directory will be used by MongoDB to store data persistently.

### Conclusion

Using MongoDB in a Docker container offers a lot of flexibility, especially for development and testing. It ensures your MongoDB instance is isolated and doesn't interfere with other projects or system settings. As someone interested in new technologies and software engineering, you might find this approach very efficient for various projects and experiments.

