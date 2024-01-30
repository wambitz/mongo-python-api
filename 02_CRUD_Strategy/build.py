import docker
from docker.errors import BuildError, APIError, ImageNotFound


def create_network(client, network_name):
    existing_networks = [net.name for net in client.networks.list()]
    if network_name in existing_networks:
        print(f"Network '{network_name}' already exists.")
    else: 
        try:
            network = client.networks.create(network_name, driver="bridge")
            print(f"Network '{network_name}' created.")
        except APIError as e:
            print(f"Error creating network: {e}")


def build_image(client, tag, path="."):
    try:
        _, build_log = client.images.build(path=path, tag=tag, rm=True)
        for line in build_log:
            if 'stream' in line:
                print(line['stream'].strip())
        print(f"Image '{tag}' built successfully.")
    except BuildError as e:
        print(f"Error building image: {e}")
    except APIError as e:
        print(f"Error with Docker API: {e}")


def check_and_pull_image(client, image_name):
    try:
        client.images.get(image_name)
        print(f"Image '{image_name}' is already available.")
    except ImageNotFound:
        print(f"Image '{image_name}' not found locally. Pulling from registry...")
        client.images.pull(image_name)
        print(f"Image '{image_name}' pulled successfully.")


if __name__ == "__main__":
    client = docker.from_env()

    network_name = "mongo-network"
    app_image_tag = "flask-app"
    base_image_name = "python:3-alpine"
    mongo_image_name = "mongo"

    create_network(client, network_name)
    check_and_pull_image(client, base_image_name)
    check_and_pull_image(client, mongo_image_name)
    build_image(client, app_image_tag)
