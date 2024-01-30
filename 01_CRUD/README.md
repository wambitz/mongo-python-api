# MongoDB and Flask Project

## Overview

This project is a Flask-based web application that interacts with a MongoDB database. It's designed to showcase the integration of a Flask app with MongoDB, using Docker for containerization and Docker Compose for managing multi-container setups.

This application is a RESTful API server built using Flask, a lightweight and flexible Python web framework, and MongoDB, a NoSQL database. It's designed to manage product and user data, allowing Create, Read, Update, and Delete (CRUD) operations on both entities.

#### Features
- **MongoDB Integration**: Utilizes MongoDB for data storage, a document-oriented database ideal for handling structured data flexibly.
- **CRUD Operations**: Supports all CRUD operations for products and users.
- **JSON Responses**: Communicates with clients using JSON, ensuring easy integration with web or mobile front-ends.

#### Endpoints
1. **Home (`/`)**: 
   - **Method**: GET
   - Returns the MongoDB server version, confirming the API's connection to the database.

2. **Product Management**:
   - **Create (`/product`)**: 
     - **Method**: POST
     - Adds a new product to the database.
   - **Read (`/product/<product_id>`)**: 
     - **Method**: GET
     - Retrieves a specific product by its ID.
   - **Update (`/product/<product_id>`)**: 
     - **Method**: PUT
     - Updates an existing product's information.
   - **Delete (`/product/<product_id>`)**: 
     - **Method**: DELETE
     - Removes a product from the database.

3. **User Management**:
   - **Create (`/user`)**: 
     - **Method**: POST
     - Adds a new user to the database.
   - **Read (`/user/<username>`)**: 
     - **Method**: GET
     - Retrieves a specific user by username.
   - **Update (`/user/<username>`)**: 
     - **Method**: PUT
     - Updates an existing user's information.
   - **Delete (`/user/<username>`)**: 
     - **Method**: DELETE
     - Removes a user from the database.

## Project Structure

- `app.py`: The main Flask application file.
- `requirements.txt`: Lists all Python dependencies for the project.
- `Dockerfile`: Instructions for building the Docker image for the Flask app.
- `docker-compose.yml`: Configuration for running the app and MongoDB using Docker Compose.
- `build.py`: Python script to automate the building of Docker images and setting up the network.
- `run.py`: Python script to run Docker containers for the Flask app and MongoDB.
- `clean.py`: Python script for stopping containers, deleting the network, and other cleanup tasks.
- `data/`: Directory to store any data files or database-related files (if applicable).
- `README.md`: This file, containing project documentation.

## Setup and Running

### Using Docker Compose

1. **Build and Run:**
   - Run `docker-compose up -d` to start the Flask app and MongoDB containers in detached mode.
2. **Check Status:**
   - Use `docker-compose ps` to check the status of the containers.
3. **View Logs:**
   - To view logs, use `docker-compose logs [service-name]`.
4. **Shutdown:**
   - To stop and remove the containers, use `docker-compose down`.

### Using Python Scripts

1. **Build:**
   - Run `python build.py` to create the Docker network, pull base images, and build the Flask app image.
2. **Run:**
   - Use `python run.py` to start the Flask app and MongoDB containers.
3. **Cleanup:**
   - To stop containers and clean up, run `python clean.py`.

## Development and Testing

- Modify `app.py` for changes in the Flask application.
- Update `requirements.txt` as needed for new Python packages.
- Use the `data/` directory for any persistent data storage needs with MongoDB.
