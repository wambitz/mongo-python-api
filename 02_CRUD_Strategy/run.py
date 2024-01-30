import docker
import os

from docker.errors import ContainerError, ImageNotFound, APIError

def run_container(client, name, image, ports, command=None, network=None, environment=None, remove=False):
    try:
        container = client.containers.run(image, 
                                          name=name, 
                                          detach=True, 
                                          ports=ports, 
                                          command=command,
                                          network=network,
                                          environment=environment, 
                                          remove=remove)
        print(f"Container '{name}' started successfully.")
    except ImageNotFound:
        print(f"Image '{image}' not found.")
    except ContainerError as e:
        print(f"Error in container '{name}': {e}")
    except APIError as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    client = docker.from_env()

    # Fetch MongoDB host from environment or use a default
    mongodb_host = os.getenv('MONGODB_HOST', 'mongo-server')

    # Flask app container
    run_container(client, 
                  name="flask-app", 
                  image="flask-app",
                  ports={'5000/tcp': 5000}, 
                  network="mongo-network",
                  environment={"MONGODB_HOST": mongodb_host},
                  remove=True)

    # MongoDB container
    run_container(client, 
                  name="mongo-server", 
                  image="mongo", 
                  ports={'27017/tcp': 27017}, 
                  network="mongo-network", 
                  remove=True)
