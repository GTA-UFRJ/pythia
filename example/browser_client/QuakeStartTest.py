import docker

# Create a Docker client object
client = docker.from_env()

# Create the container
container = client.containers.create(
    "treyyoder/quakejs:latest",
    name="quakejs",
    environment={"HTTP_PORT": "8080"},
    ports={"80": 8080, "27960": 27960}
)

# Start the container
container.start()

container.wait()

print(f"Container ID: {container.id}")