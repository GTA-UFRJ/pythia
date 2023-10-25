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
                           volumes=[app.volume+":/output"],
                           cap_add=["NET_ADMIN"])
  connect(app, network, app.ip)


def create_mec_app(app, network):
  """This function creates an app container without running it.
  Parameters:
    app: the app to run
    host: the PythiaMECApp object 
  """

  logging.info(f"Creating container {app.docker_id} from {app.image}, "+
      f"with ip={app.ip}.")
  client.containers.create(app.image,
                           name=app.docker_id,
                           hostname=app.name,
                           cap_add=["NET_ADMIN"])
  connect(app, network, app.ip)

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
                         driver="bridge",
                         attachable=True,
                         ipam=ipam_config,
                         options={
                         "com.docker.network."+
                         "container_iface_prefix":network.interface_prefix})



def connect(docker_container, network, ip):
  """This function connects docker_container to the network"""
  c = client.containers.get(docker_container.docker_id)
  network.docker_obj.connect(c,ipv4_address=ip)


def connect_app_to_host(app):
  """This function connects an UEApp to its vUE or
  a MECApp to its vMEC."""
  gateway_ip = app.host.external_ip
  cmd = "ip route del default"
  execute_cmd(cmd, app.docker_id)
  cmd = f"ip route add default via {gateway_ip}"
  execute_cmd(cmd, app.docker_id)
  return 0

def connect_app_to_app(ue_app, mec_app):
  """This function connects two apps, using their 
  hosts to route packets."""
  cmd = f"ip route add {ue_app.ip} via {ue_app.host.infra_ip}"
  execute_cmd(cmd, mec_app.host.docker_id)

  cmd = f"ip route add {mec_app.ip} via {mec_app.host.infra_ip}"
  execute_cmd(cmd, ue_app.host.docker_id)

def execute_cmd(cmd, container_id):
  """This function executes the command cmd 
  in container represented by container id"""
  container = client.containers.get(container_id)
  return container.exec_run(cmd)

def change_link(ue_app, mec_app,
                ue_network, mec_network,
                bitrate, delay, distribution=0):
  """
  This function changes the link between two pythia apps.
  bitrate is on kbits
  delay and distribution are in ms.
  """

  #Execute on host a
  change_link_on_host(ue_app, mec_app.ip, ue_network.interface,
                      bitrate, delay)

  #Execute on host b
  change_link_on_host(mec_app, ue_app.ip, mec_network.interface,
                      bitrate, delay)


def change_link_on_host(host, ip_dst, interface,
                        bitrate, delay):

  cmds = [f"tc qdisc add dev {interface} root handle 1: prio",
  f"tc qdisc add dev {interface} parent 1:3 "+
  f"handle 30: tbf rate {bitrate}kbit buffer 1600 limit 3000",

  f"tc qdisc add dev {interface} parent 30:1 "+
  f"handle 31: netem delay {delay}ms",
  

  f"tc filter add dev {interface} protocol ip parent "+
  f"1:0 prio 3 u32 match ip dst {ip_dst} flowid 1:3"]

  #logging.info(f"=== Executing commands on {host.docker_id}")
  for cmd in cmds:
    #logging.info(cmd)
    execute_cmd(cmd, host.docker_id)
