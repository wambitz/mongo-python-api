import docker
from docker.errors import NotFound


def stop_and_remove_container(client, container_name):
    """Stops and removes a specified Docker container.

    This function attempts to stop and forcibly remove a Docker container by its name. It handles
    cases where the container might not exist (either already stopped or removed) and logs appropriate
    messages to the console.

    Args:
        client: A Docker client object created with docker.from_env() or similar.
        container_name: The name of the Docker container to stop and remove.

    Raises:
        docker.errors.APIError: An error occurred when attempting to stop or remove the container due to issues with Docker API.
    """
    try:
        container = client.containers.get(container_name)
        container.stop()  # Stops the container
        container.remove(force=True)  # Forcibly removes the container
        print(f"Container '{container_name}' stopped and forcibly removed.")
    except NotFound:
        print(
            f"Container '{container_name}' not found. It might be already stopped or removed."
        )
    except docker.errors.APIError as e:
        print(f"Error removing container '{container_name}': {e}")


def remove_network(client, network_name):
    """Removes a specified Docker network.

    This function tries to remove a Docker network by its name. It deals with cases where the network
    may not be found (potentially already removed) and logs appropriate messages to the console.

    Args:
        client: A Docker client object.
        network_name: The name of the Docker network to remove.

    Raises:
        docker.errors.APIError: An error occurred when attempting to remove the network due to issues with Docker API.
    """
    try:
        network = client.networks.get(network_name)
        network.remove()
        print(f"Network '{network_name}' removed.")
    except NotFound:
        print(f"Network '{network_name}' not found. It might be already removed.")
    except APIError as e:
        print(f"Error removing network '{network_name}': {e}")


if __name__ == "__main__":
    client = docker.from_env()

    # List of container names to stop and remove
    container_names = ["flask-app", "mongodb-server"]

    for name in container_names:
        stop_and_remove_container(client, name)

    # Name of the network to remove
    network_name = "app-network"
    remove_network(client, network_name)
