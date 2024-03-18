import docker
import os

from docker.errors import ContainerError, ImageNotFound, APIError


def run_container(
    client,
    name,
    image,
    ports,
    command=None,
    network=None,
    environment=None,
    remove=False,
    working_dir=None,
):
    """
    Starts a Docker container based on the specified parameters.

    This function attempts to run a Docker container using the provided image and configuration. It
    supports setting the container's name, ports, network, environment variables, and working directory.
    The function handles exceptions related to image availability, container errors, and API issues, logging
    appropriate messages. It can optionally remove the container upon exit.

    Args:
        client: A Docker client object created with docker.from_env() or similar.
        name: A string specifying the name of the container.
        image: A string specifying the Docker image to use for the container.
        ports: A dictionary mapping container ports to host ports, e.g., {"container_port/tcp": host_port}.
        command: Optional; the command to run in the container.
        network: Optional; the network to connect the container to.
        environment: Optional; a dictionary of environment variables to set in the container.
        remove: Optional; a boolean indicating whether to automatically remove the container when it exits.
        working_dir: Optional; the working directory to set for the command to run in.

    Returns:
        A Docker container object if the container starts successfully. None if an error occurs.

    Raises:
        ImageNotFound: Raised when the specified Docker image is not available.
        ContainerError: Raised when there's an error in container execution.
        APIError: Raised when the Docker API encounters an error.
        Exception: Catches and logs unexpected errors during container run.
    """
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
            working_dir=working_dir,
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
    mongodb_host = os.getenv("MONGODB_HOST", "mongodb-server")

    # Flask app container
    run_container(
        client,
        name="flask-app",
        image="flask-app",
        ports={"5000/tcp": 5000},
        network="app-network",
        environment={"MONGODB_HOST": mongodb_host},
        remove=True,
        working_dir="/02_CRUD_Strategy",
    )

    # MongoDB container
    run_container(
        client,
        name="mongodb-server",
        image="mongo",
        ports={"27017/tcp": 27017},
        network="app-network",
        remove=True,
    )
