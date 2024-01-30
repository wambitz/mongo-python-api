import docker
from docker.errors import NotFound, APIError

def stop_and_remove_container(client, container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        print(f"Container '{container_name}' stopped and removed.")
    except NotFound:
        print(f"Container '{container_name}' not found.")
    except APIError as e:
        print(f"Error with Docker API: {e}")

def remove_network(client, network_name):
    try:
        network = client.networks.get(network_name)
        network.remove()
        print(f"Network '{network_name}' removed.")
    except NotFound:
        print(f"Network '{network_name}' not found.")
    except APIError as e:
        print(f"Error with Docker API: {e}")

if __name__ == "__main__":
    client = docker.from_env()

    stop_and_remove_container(client, "flask-app")
    stop_and_remove_container(client, "mongo-server")
    remove_network(client, "mongo-network")
