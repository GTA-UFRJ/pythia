"""This file gathers functions related to docker"""
import subprocess
import os, sys
import docker
import logging
import ipaddress

#Obtaining docker client
client = docker.from_env()

def swarm_init():
  # Initializes the swarm
  try:
      response = client.swarm.init()
      print("Swarm initialized successfully.")

      # Retrieve swarm information
      swarm_info = client.swarm.attrs

      # Print the command to join as a worker
      worker_token = swarm_info.get('JoinTokens', {}).get('Worker')
      if worker_token:
          print(f"Command to join as a worker: docker swarm join --token {worker_token} {client.info().get('Swarm', {}).get('RemoteManagers', [{}])[0].get('Addr')}")

      # Print the command to join as a manager
      manager_token = swarm_info.get('JoinTokens', {}).get('Manager')
      if manager_token:
          print(f"Command to join as a manager: docker swarm join --token {manager_token} {client.info().get('Swarm', {}).get('RemoteManagers', [{}])[0].get('Addr')}")

  except docker.errors.APIError as e:
      if "This node is already part of a swarm" in str(e):
          print("This node is already part of a swarm.")
      else:
          print(f"Failed to initialize swarm: {e}")
      sys.exit(1)
  return 0

def create_host_service(host, infra_network, external_network):
  """This function creates a Docker service without running it.
  Parameters:
    host: the PythiaEmulationHost object
  """
  logging.info(f"Creating service {host.docker_id} from {host.image}, " +
                f"with infra_ip={host.infra_ip}, and external_ip={host.external_ip}.")

  # Define the service configuration
  service_config = {
      'name': host.docker_id,
      'image': host.image,
      'cap_add': ["NET_ADMIN"],
      'networks': [infra_network.name, external_network.name]
  }

  # Create the service
  client.services.create(**service_config)

  service = client.services.get(host.docker_id)
  while not service.tasks()[0]['Status']['State'] == 'running':
    service.reload()

  return 0

def create_host(host, infra_network, external_network):
  """This function creates a host container without running it.
  Parameters:
    host: the PythiaEmulationHost object 
  """
  logging.info(f"Creating container {host.docker_id} from {host.image}, "+
    f"with infra_ip={host.infra_ip}, and external_ip={host.external_ip}.")
  client.containers.create(host.image,
                            name=host.docker_id,
                            cap_add=["NET_ADMIN"])
  connect(host, infra_network, host.infra_ip)
  connect(host, external_network, host.external_ip)
  return 0

def remove_container(container):
  """This function removes the container that
  runs host on docker"""
  c = client.containers.get(container.docker_id)
  c.stop()
  c.remove()

def start_container(container):
  c = client.containers.get(container.docker_id)
  c.start()

def create_volume(app):
  """This function creates a volume without attaching it to a
  container"""
  print(app.volume)
  client.volumes.create(name = app.volume)

def create_ue_volume(app):
  """This function creates a ue volume without attaching it to a
  container"""

  for volume in app.volume:
    if ":/output" in volume:
      ue_name = volume.split(":")[0]
      client.volumes.create(name = ue_name)

def create_mec_app(app, network):
  """This function creates an app container without running it.
  Parameters:
    app: the app to run
    host: the PythiaMECApp object 
  """

  logging.info(f"Creating container {app.docker_id} from {app.image}, "+
      f"with ip={app.ip}.")
  
  params = {
      "image": app.image,
      "name": app.docker_id,
      "hostname" : app.name,
      "cap_add": ["NET_ADMIN"],
  }
  
  # Add volume if it exists
  if app.environment:
    params["environment"] = app.environment
  if app.ports:
    params["ports"] = app.ports

  logging.info(f"Creating mec app with params {params}")
  # Call the create function with the dynamically built parameters
  client.containers.create(**params)

  # Connect the created container to the specified network with the given IP
  logging.info(f"Connecting mec app to {network} with ip {app.ip}")
  connect(app, network, app.ip)

def create_ue_app(app, network):
  """This function creates an app container without running it.
  Parameters:
    app: the app to run
    network: the network to connect the app container to
  """
  logging.info(f"Creating container {app.docker_id} from {app.image}, " +
                f"with ip={app.ip}.")
  
  # Initialize the base parameters for the container creation
  params = {
      "image": app.image,
      "name": app.docker_id,
      "command": app.command,
      "cap_add": ["NET_ADMIN"],
  }
  
  # Add volume if it exists
  if app.volume:
    params["volumes"] = app.volume
  if app.devices:
    params["devices"] = app.devices
  if app.environment:
    params["environment"] = app.environment
  if app.ports:
    params["ports"] = app.ports

  logging.info(f"Creating ue app with params {params}.")

  # Call the create function with the dynamically built parameters
  client.containers.create(**params)

  # Connect the created container to the specified network with the given IP
  connect(app, network, app.ip)

def create_ue_app_service(app, network):
  """This function creates and runs an app service based on provided configuration.
  Parameters:
      app: the app to run
      network: the network to connect the app service to
  """
  logging.info(f"Creating service {app.docker_id} from {app.image}, " +
                f"with ip={app.ip}.")

  # Initialize the base parameters for the service creation
  params = {
      "image": app.image,          # The image used for the service
      "name": app.docker_id,       # Service name (unique identifier)
      "command": app.command,      # Command to run in the service
      "cap_add": ["NET_ADMIN"],    # Required capability
      "networks": [network.name],  # Network to connect the service
  }

  if app.volume:
      params["mounts"] = [{"source": v.split(":")[0], "target": v.split(":")[1], "type": "volume"} for v in app.volume]
  if app.environment:
      params["env"] = app.environment

  logging.info(f"Creating ue app service with params {params}.")

  # Create the service using Docker's Python API
  service = client.services.create(**params)

  # Wait for the service to start running
  while service.tasks()[0]['Status']['State'] != 'running':
      service.reload()

def delete_network(network):
  """This function deletes the docker network
  associated with the PythiaNetwork network"""
  try:
    n = client.networks.get(network.name)
    n.remove()
  except docker.errors.NotFound:
    pass

def create_network(network):
  """This function creates a docker network from a
  PythiaNetwork. If a network with the same
  name already exists, it is removed"""
  delete_network(network)

  ipam_pool = docker.types.IPAMPool(subnet=network.ip_range)
  ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
  network.docker_obj = client.networks.create(
                         network.name,
                         driver="overlay",
                         attachable=True,
                         ipam=ipam_config,
                         options={"com.docker.network.container_iface_prefix":network.interface_prefix})


def connect(docker_container, network, ip):
  """This function connects docker_container to the network"""
  c = client.containers.get(docker_container.docker_id)
  network.docker_obj.connect(c,ipv4_address=ip)

def connect_app_to_host(app,
                        network_interface,
                        other_network_range):
  """This function connects an UEApp to its vUE or
  a MECApp to its vMEC."""
  # cmd = "apt install iproute2 -y"
  # execute_cmd(cmd, app.docker_id)
  #gateway_ip = app.host.external_ip
  #cmd = "ip route del default"
  #execute_cmd(cmd, app.docker_id)
  #cmd = f"ip route add default via {gateway_ip} dev {network_interface}"
  cmd = f"ip route add {other_network_range} via {app.host.external_ip}"
  execute_cmd(cmd, app.docker_id)
  return 0

def connect_app_to_app(ue_app,
                       ue_network_range,
                       mec_app,
                       mec_network_range):
  """This function connects two apps, using their 
  hosts to route packets."""

  #cmd = "ip route del default"
  #execute_cmd(cmd, mec_app.host.docker_id)
  #execute_cmd(cmd, ue_app.host.docker_id)

  #ue_app_subnet = get_subnet_ip(ue_app.ip, 16)
  #mec_app_subnet = get_subnet_ip(mec_app.ip, 16)

  cmd = f"ip route add {ue_network_range} via {ue_app.host.infra_ip}"
  execute_cmd(cmd, mec_app.host.docker_id)

  cmd = f"ip route add {mec_network_range} via {mec_app.host.infra_ip}"
  execute_cmd(cmd, ue_app.host.docker_id)

def execute_cmd(cmd, container_id):
  """This function executes the command cmd 
  in container represented by container id"""
  container = client.containers.get(container_id)
  return container.exec_run(cmd)

def execute_cmd2(cmd, service_name):
  """
  This function executes the command cmd 
  in the first available container of the service represented by service_name.
  """
  # Get the list of tasks for the given service
  service = client.services.get(service_name)
  tasks = service.tasks(filters={'desired-state': 'running'})

  if not tasks:
      raise ValueError(f"No running tasks found for service: {service_name}")

  # Get the container ID from the first task (you may need to adapt this for your use case)
  container_id = tasks[0]['Status']['ContainerStatus']['ContainerID']

  # Execute the command in the container
  container = client.containers.get(container_id)
  return container.exec_run(cmd)

def rename_container_interface(network_range, network_interface, container_id):
  subnet_fixed_positions = get_network_prefix(network_range)

  # print(f'sh -c "ip -o addr show | grep \'{subnet_fixed_positions}\' | awk \'{{print $2}}\' | cut -d \':\' -f1"')
  interface = execute_cmd2(f'sh -c "ip -o addr show | grep \'{subnet_fixed_positions}\' | awk \'{{print $2}}\' | cut -d \':\' -f1"', container_id)[1].decode().strip()
  # print(interface)

  # print(f'sh -c "ip link set {interface} down; ip link set {interface} name {network_interface} ; ip link set {network_interface} up"')
  execute_cmd2(f'sh -c "ip link set {interface} down; ip link set {interface} name {network_interface} ; ip link set {network_interface} up"', container_id)[1]

def start_link(vUE, vmec_host,
                network, distribution=0):
  """
  This function changes the link between two pythia apps.
  bitrate is on kbits
  delay and distribution are in ms.
  """
  #Execute on host a
  logging.info(f"Start from {vUE.docker_id} to {vmec_host.docker_id}.")
  start_link_on_host(vUE, vmec_host, network.interface,'vUE')

  #Execute on host b
  logging.info(f"Start from {vmec_host.docker_id} to {vUE.docker_id}.")
  start_link_on_host(vmec_host, vUE, network.interface,'vmec')

def start_link_on_host(host, dst, interface, side):
  queue = host.queue_name.get(dst.infra_ip)
  if side == 'vUE':
    for app in dst.active_apps:
      cmds = [f"tc qdisc add dev {interface} root handle 1: htb default 1", 
            f"tc class add dev {interface} parent 1: classid {queue} htb rate 10000 ceil 640kbps",
            f"tc qdisc add dev {interface} parent {queue} handle 4{queue.split(':')[1]}: netem delay 1ms",
            f"tc filter add dev {interface} parent 1:0 prio 0 u32 match ip dst {app.ip} flowid {queue}",
            f"ping -c 1 {app.ip}"]
      for cmd in cmds:
        execute_cmd(cmd, host.docker_id)
        
  else:
    for app in dst.apps:
      cmds = [f"tc qdisc add dev {interface} root handle 1: htb default 1", 
            f"tc class add dev {interface} parent 1: classid {queue} htb rate 10000 ceil 640kbps",
            f"tc qdisc add dev {interface} parent {queue} handle 4{queue.split(':')[1]}: netem delay 1ms",
            f"tc filter add dev {interface} parent 1:0 prio 0 u32 match ip dst {app.ip} flowid {queue}",
            f"ping -c 1 {app.ip}"]
      for cmd in cmds:
        execute_cmd(cmd, host.docker_id)


def change_link(vUE, vmec_host,
                network,
                bitrate, delay, distribution=0):
  """
  This function changes the link between two pythia apps.
  bitrate is on kbits
  delay and distribution are in ms.
  """
  #logging.info("Vou mudar")
  #Execute on host a
  logging.info(f"From {vUE.docker_id} to {vmec_host.docker_id}.")
  change_link_on_host(vUE, vmec_host, network.interface,
                      bitrate, float(delay)/2, 'vUE')

  #Execute on host b
  logging.info(f"From {vmec_host.docker_id} to {vUE.docker_id}.")
  change_link_on_host(vmec_host, vUE, network.interface,
                      bitrate, float(delay)/2, 'vmec')
  #logging.info("Mudei")

def change_link_on_host(host, dst, interface,
                        bitrate, delay, side):

  queue = host.queue_name.get(dst.infra_ip)
  if side == 'vUE':
    for app in dst.active_apps:
      cmds = [f"tc class change dev {interface} parent 1: classid {queue} htb rate {bitrate} ceil 640kbps",
            f"tc qdisc change dev {interface} parent {queue} handle 4{queue.split(':')[1]}: netem delay {delay}ms loss 0%"]
      for cmd in cmds:
        execute_cmd(cmd, host.docker_id)
        
  else:
    for app in dst.apps:
      cmds = [f"tc class change dev {interface} parent 1: classid {queue} htb rate {bitrate} ceil 640kbps",
            f"tc qdisc change dev {interface} parent {queue} handle 4{queue.split(':')[1]}: netem delay {delay}ms loss 0%"]
      for cmd in cmds:
        execute_cmd(cmd, host.docker_id)

def old_change_link(ue_app, mec_app,
                ue_network, mec_network,
                bitrate, delay, distribution=0):
  """
  This function changes the link between two pythia apps.
  bitrate is on kbits
  delay and distribution are in ms.
  """
  logging.info("Vou mudar")
  #Execute on host a
  old_change_link_on_host(ue_app, mec_app.ip, ue_network.interface,
                      bitrate, float(delay)/2)

  #Execute on host b
  old_change_link_on_host(mec_app, ue_app.ip, mec_network.interface,
                      bitrate, float(delay)/2)
  logging.info("Mudei")


def old_change_link_on_host(host, ip_dst, interface,
                        bitrate, delay):
  
  cmds = [f"tc qdisc replace dev {interface} root handle 1: prio",
  f"tc qdisc replace dev {interface} parent 1:3 "+
  f"handle 30: tbf rate {bitrate}kbit buffer 1600 limit 3000",

  f"tc qdisc replace dev {interface} parent 30:1 "+
  f"handle 31: netem delay {delay}ms",
  
  f"tc filter replace dev {interface} protocol ip parent 1: prio 3 "+
  f"u32 match ip dst {ip_dst} flowid 1:3"]

  for cmd in cmds:
    result = str(execute_cmd(cmd, host.docker_id).output)
    #logging.info(result)

def create_api_container(app, network):
  client.containers.create(app.image,
                             name=app.docker_id,
                             command=app.command,
                             cap_add=["NET_ADMIN"])
  logging.info(f'IP is {app.ip}')
  connect(app, network, app.ip)
  return 0

def get_subnet_ip(ip, bits):
  ip_parts = ip.split('.')
  subnet_ip_parts = ip_parts[:bits // 8]
  subnet_ip_parts += ['0'] * (4 - len(subnet_ip_parts))
  subnet_ip = '.'.join(subnet_ip_parts)
  return subnet_ip

def get_network_prefix(subnet_str):
    """
    This function extracts the non-zero octets (fixed part) of the network address.
    
    Examples:
    - get_network_prefix("192.168.0.0/16") -> "192.168."
    - get_network_prefix("172.21.0.0/12") -> "172.16."
    - get_network_prefix("10.0.0.0/8") -> "10."
    """
    subnet = ipaddress.ip_network(subnet_str, strict=False)
    network_address = subnet.network_address
    fixed_positions = ''
    for octet in str(network_address).split('.'):
        if octet != '0':
            fixed_positions += octet + '.'
    return fixed_positions