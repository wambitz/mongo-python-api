import docker
import os

from docker.errors import ContainerError, ImageNotFound, APIError


def run_container(client, name, image, ports, command=None, network=None, environment=None, remove=False, working_dir=None):
    """Attempts to start a Docker container with the specified configuration."""
    try:
        container = client.containers.run(
            image,
            name=name,
            detach=True,
            ports=ports,
            command=command,
            network=network,
            environment=environment,
            auto_remove=remove,  # 'auto_remove' is the correct argument name
            working_dir=working_dir
        )
        print(f"Container '{name}' started successfully.")
        return container  # Returning the container could be useful for further manipulation or inspection
    except ImageNotFound:
        print(f"Image '{image}' not found.")
    except ContainerError as e:
        print(f"Error in container '{name}': {e}")
    except APIError as e:
        print(f"API Error: {e}")
    except Exception as e:  # Catch-all for any other exceptions
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    client = docker.from_env()

    # Fetch MongoDB host from environment or use a default
    mongodb_host = os.getenv('MONGODB_HOST', 'mongodb-server')

    # Flask app container
    run_container(client, 
                  name="flask-app", 
                  image="flask-app",
                  ports={'5000/tcp': 5000}, 
                  network="app-network",
                  environment={"MONGODB_HOST": mongodb_host},
                  remove=True,
                  working_dir="/02_CRUD_Strategy")

    # MongoDB container
    run_container(client, 
                  name="mongodb-server", 
                  image="mongo", 
                  ports={'27017/tcp': 27017}, 
                  network="app-network", 
                  remove=True)
