"""This file gathers functions related to docker"""
import subprocess
import os
import docker
import logging

#Obtaining docker client
client = docker.from_env()

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

    logging.info(f"Creating host {host.name}")
    connect(host, infra_network.docker_obj, host.infra_ip)
    logging.info("Connected infra ip")
    connect(host, external_network.docker_obj, host.external_ip)
    logging.info("Connected external ip")
    return 0

def remove_container(container):
  """This function removes the container that
  runs host on docker"""
  c = client.containers.get(container.docker_id)
  c.stop()
  c.remove()

def start_container(container):
  logging.info(f"Starting container {container.docker_id}")
  c = client.containers.get(container.docker_id)
  c.start()

def create_external_app(app,network):
  """This function creates an app container without running it.
  Parameters:
    app: the app to run
    host: the PythiaApp object 
  """
  logging.info(f"Creating container {app.docker_id} from {app.image}, "+
      f"with ip={app.ip}.")
  client.containers.create(app.image,
                           name=app.docker_id,
                           cap_add=["NET_ADMIN"])
  connect(app, network.docker_obj, app.ip)


def create_mec_app(app, network):
  """This function creates an app container without running it.
  Parameters:
    app: the app to run
    host: the PythiaMECApp object 
  """
  client.containers.create(app.image,
                           name=app.docker_id,
                           hostname=app.name,
                           cap_add=["NET_ADMIN"])
  connect(app, network.docker_obj, app.ip)

def create_ue_app(app, network):
  """This function creates an app container without running it.
  Parameters:
    app: the app to run
    host: the PythiaUEApp object 
  """
  create_external_app(app,network)

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

  ipam_pool = docker.types.IPAMPool(
                           subnet=network.ip_range)

  ipam_config = docker.types.IPAMConfig(
    pool_configs=[ipam_pool])

  network.docker_obj = client.networks.create(
                         network.name,
                         driver="overlay",
                         attachable=True,
                         ipam=ipam_config)

def connect(docker_container, docker_network, ip):
  """This function connects docker_container to the network"""
  c = client.containers.get(docker_container.docker_id)
  docker_network.connect(c,ipv4_address=ip)


def connect_app_to_host(app):
  """This function connects an UEApp to its vUE or
  a MECApp to its vMEC."""
  gateway_ip = app.host.external_ip
  cmd = "ip route del default"
  logging.info(f"Executing {cmd} to {app.docker_id}")
  execute_cmd(cmd, app.docker_id)
  cmd = f"ip route add default via {gateway_ip}"
  logging.info(f"Executing {cmd} to {app.docker_id}")
  execute_cmd(cmd, app.docker_id)
  return 0

def connect_app_to_app(ue_app, mec_app):
  """This function connects two apps, using their 
  hosts to route packets."""
  #v_mec ip route add (ue_net) via (ip  do v_ue na core_net)
  cmd = f"ip route add {ue_app.ip} via {ue_app.host.infra_ip}"
  logging.info(f"Executing {cmd} to {mec_app.host.docker_id}")
  execute_cmd(cmd, mec_app.host.docker_id)
  #execute_cmd(cmd, app.docker_id)

  #v_ue ip route add (mec_net) via (ip do v_mec na core_net)
  cmd = f"ip route add {mec_app.ip} via {mec_app.host.infra_ip}"
  logging.info(f"Executing {cmd} to {ue_app.host.docker_id}")
  execute_cmd(cmd, ue_app.host.docker_id)

def execute_cmd(cmd, container_id):
  """This function executes the command cmd 
  in container represented by container id"""
  container = client.containers.get(container_id)
  return container.exec_run(cmd)

