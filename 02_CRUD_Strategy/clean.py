import docker
from docker.errors import NotFound


def stop_and_remove_container(client, container_name):
    """Stop and remove a Docker container by its name."""
    try:
        container = client.containers.get(container_name)
        container.stop()  # Stops the container
        container.remove(force=True)  # Forcibly removes the container
        print(f"Container '{container_name}' stopped and forcibly removed.")
    except NotFound:
        print(f"Container '{container_name}' not found. It might be already stopped or removed.")
    except docker.errors.APIError as e:
        print(f"Error removing container '{container_name}': {e}")


def remove_network(client, network_name):
    """Remove a Docker network by its name."""
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