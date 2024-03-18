import docker
from docker.errors import BuildError, APIError, ImageNotFound


def create_network(client, network_name):
    """Ensure the Docker network exists or create it if it doesn't."""
    try:
        network = client.networks.get(network_name)
        print(f"Network '{network_name}' already exists.")
    except docker.errors.NotFound:
        try:
            network = client.networks.create(network_name, driver="bridge")
            print(f"Network '{network_name}' created.")
        except APIError as e:
            print(f"Error creating network: {e}")


def build_image(client, tag, path="."):
    """Build a Docker image from a Dockerfile."""
    try:
        _, build_log = client.images.build(path=path, tag=tag, rm=True)
        for line in build_log:
            if "stream" in line:
                print(line["stream"].strip())
        print(f"Image '{tag}' built successfully.")
    except BuildError as e:
        print(f"Error building image: {e}")
    except APIError as e:
        print(f"Error with Docker API: {e}")


def check_and_pull_image(client, image_name):
    """Check for an image locally and pull it if not found."""
    try:
        client.images.get(image_name)
        print(f"Image '{image_name}' is already available.")
    except ImageNotFound:
        print(f"Image '{image_name}' not found locally. Pulling from registry...")
        client.images.pull(image_name)
        print(f"Image '{image_name}' pulled successfully.")


if __name__ == "__main__":
    client = docker.from_env()

    network_name = "app-network"
    app_image_tag = "flask-app"
    base_image_name = "python:3-alpine"
    mongo_image_name = "mongo"

    create_network(client, network_name)
    check_and_pull_image(
        client, base_image_name
    )  # Optional based on your Docker Compose setup
    check_and_pull_image(
        client, mongo_image_name
    )  # Useful if you want to ensure MongoDB image is pre-pulled
    build_image(client, app_image_tag, "..")
