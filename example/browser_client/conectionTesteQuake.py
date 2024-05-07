import docker

# Docker client
client = docker.from_env()

def run_firefox_on_network(network_name):
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

def run_quakejs_on_network(network_name):
    """Run QuakeJS container and connect it to the specified network"""
    print("start quake")
    container = client.containers.create(
        'treyyoder/quakejs:latest',
        environment={'HTTP_PORT': '8080'},
        ports={'80/tcp': 8080, '27960/tcp': 27960},
        network=network_name
    )

    container.start()
    print("quake created")
    return container

# Create a Docker network
network_name = 'my_network'
network = client.networks.create(network_name, driver='bridge')

# Run QuakeJS container and connect it to the network
quakejs_container = run_quakejs_on_network(network_name)

print("rodou quake")

# Get the IP address of the QuakeJS container
quakejs_ip = quakejs_container.attrs['NetworkSettings']['IPAddress']

# Run Firefox container and connect it to the network
firefox_container = run_firefox_on_network(network_name)

# Get the IP address of the Firefox container
firefox_ip = firefox_container.attrs['NetworkSettings']['IPAddress']

print("Firefox container IP:", firefox_ip)
print("QuakeJS container IP:", quakejs_ip)

# Manually handle removal of the container after it stops running
firefox_container.wait()
quakejs_container.wait()

firefox_container.remove()
quakejs_container.remove()
