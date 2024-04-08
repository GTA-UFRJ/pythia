import docker

def run_firefox():
    client = docker.from_env()
    
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
    network_mode = 'host'
    command = '--class=firefox-docker http://localhost:8080'

    container = client.containers.create(
        'firefox:latest',
        command=command,
        volumes=volumes,
        environment=environment,
        devices=device,
        network_mode=network_mode
    )

    container.start()

    # Manually handle removal of the container after it stops running
    container.wait()
    container.remove()

if __name__ == "__main__":
    run_firefox()