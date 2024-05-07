import docker

# Docker client
client = docker.from_env()

def run_firefox_on_network(network_name, simple_server_ip):
    """Run Firefox container and connect it to the specified network"""
    volumes = [
        '/tmp/.X11-unix:/tmp/.X11-unix',
        '/dev/shm:/dev/shm',
        '/run/user/1000/pulse:/run/user/1000/pulse'
    ]

    environment = [
        'DISPLAY=:0',
        'PULSE_SERVER=unix:/run/user/1000/pulse/native'
    ]
    
    device = ['/dev/dri']
    network_mode = network_name
    command = f'--class=firefox-docker'

    container = client.containers.create(
        'firefox:latest',
        command=command,
        volumes=volumes,
        environment=environment,
        devices=device,
        network=network_name,
    )

    container.start()

    return container

def run_simple_server_on_network(network_name):
    """Run Simple Server container and connect it to the specified network"""
    container = client.containers.create('simple_server', network=network_name)
    container.start()
    return container

# Create a Docker network
network_name = 'my_network'
network = client.networks.create(network_name, driver='bridge')

# Run Simple Server container and connect it to the network
simple_server_container = run_simple_server_on_network(network_name)

# Get the IP address of the Simple Server container
simple_server_ip = simple_server_container.attrs['NetworkSettings']['IPAddress']

# Run Firefox container and connect it to the network
firefox_container = run_firefox_on_network(network_name, simple_server_ip)

# Get the IP address of the Firefox container
firefox_ip = firefox_container.attrs['NetworkSettings']['IPAddress']

print("Firefox container IP:", firefox_ip)
print("Simple Server container IP:", simple_server_ip)

# Manually handle removal of the container after it stops running
firefox_container.wait()
simple_server_container.wait()

firefox_container.remove()
simple_server_container.remove()
