"""This file runs the emulation stage of Pythia"""


"""TODO:
Emulation must create UEApp, vUE, and vMEC containers.
The MEC Platform should be responsible for MECApp creation"""

import pythia.docker_utils as docker_utils
import pythia.structures as structures
import logging
import sys
import time
import docker

logging.basicConfig(level=logging.INFO)

def emulate(networks, links):
  """This function runs the emulation phase of Pythia"""

  # Create emulation events queue
  emu_times = []
  events_queue = links
  events_queue.sort(key=lambda x: x.time, reverse=True)
  emulation_zero = time.time()
  emulation_time_error = 0.1
  event = events_queue.pop()
  # Start main emulation loop
  while(len(events_queue)):
    emulation_time = time.time() - emulation_zero
    time_difference = event.time - emulation_time
    if time_difference < emulation_time_error:
      logging.info(f"Event time = {event.time}, emu time = {emulation_time}, Time diff = {time_difference}")
      docker_utils.change_link(event.ue, event.mec_host,
                              networks['infra'],
                              event.upload, event.latency)
      emu_times.append([emulation_time, time.time() - emulation_time ])
      event = events_queue.pop()
      time_difference = event.time - emulation_time
    if time_difference < 0:
      continue
    time.sleep(time_difference - emulation_time_error/2)
    print(f"Event = {event}")
  #while True:
  #pass

def bootstrap(networks, mec_hosts, mec_apps, UEs, links, server_ip):
  # Need to create the ping_sender and ping_receiver containers.
  """This function bootstraps the emulation.
  It creates the emulation scenario inside docker, 
  with UEs and MECHosts, their networks and ips."""

  # Initializes the swarm
  docker_utils.swarm_init()

  #Create networks
  for net in networks:
    docker_utils.create_network(networks[net])

  #Allocate mec_apps ip's before allocating
  # ip's to the virtual mec hosts
  for mec_app in mec_apps:
    mec_apps[mec_app].ip = networks['mec'].allocate_ip(mec_apps[mec_app].ip) 

  #Create MECHosts
  for vmh in mec_hosts:
    mec_hosts[vmh].infra_ip = networks['infra'].allocate_ip()
    mec_hosts[vmh].external_ip = networks['mec'].allocate_ip()

    docker_utils.create_host_service(mec_hosts[vmh],
                                    networks['infra'],
                                    networks['mec'])
    
    docker_utils.rename_container_interface(networks['infra'].ip_range,
                                            networks['infra'].interface,
                                            mec_hosts[vmh].docker_id) ######################
    docker_utils.rename_container_interface(networks['mec'].ip_range,
                                            networks['mec'].interface,
                                            mec_hosts[vmh].docker_id) #####################

  #Create UEs
  for vUE in UEs:
    UEs[vUE].infra_ip = networks['infra'].allocate_ip()
    UEs[vUE].external_ip = networks['ue'].allocate_ip()
    docker_utils.create_host_service(UEs[vUE],
                             networks['infra'],
                             networks['ue']) ######################
    docker_utils.rename_container_interface(networks['infra'].ip_range,
                                            networks['infra'].interface,
                                            UEs[vUE].docker_id) ######################
    docker_utils.rename_container_interface(networks['ue'].ip_range,
                                            networks['ue'].interface,
                                            UEs[vUE].docker_id) ######################

    #Start apps on each vUE
    #TODO: Set this on emulation start
    for ue_app in UEs[vUE].apps:
      ue_app.ip = networks['ue'].allocate_ip()
      ue_app.host = UEs[vUE]
      docker_utils.create_ue_volume(ue_app) ######################
      print(f"UE ports = {ue_app.ports}")
      docker_utils.create_ue_app_service(ue_app, networks['ue']) ######################
      docker_utils.rename_container_interface(networks['ue'].ip_range,
                                            networks['ue'].interface,
                                            ue_app.docker_id) ######################
      while True:
        pass
      docker_utils.connect_app_to_host(ue_app,
                                       networks['ue'].interface,
                                       networks['mec'].ip_range) ######################

  #Start MEC apps. Allocate them to first host
  #Todo: start MEC Apps through MEC System.
  mec_host = mec_hosts[list(mec_hosts.keys())[0]]
  for mec_app in mec_apps:
    mec_apps[mec_app].host = mec_host
    mec_host.active_apps.add(mec_apps[mec_app])
    docker_utils.create_mec_app(mec_apps[mec_app], networks['mec']) ######################

    #Set route to this mec_app
    for vUE in UEs:
      for ue_app in UEs[vUE].apps:
        docker_utils.connect_app_to_app(ue_app,
                                        networks['ue'].ip_range,
                                        mec_apps[mec_app],
                                        networks['mec'].ip_range) ######################

    docker_utils.start_container(mec_apps[mec_app]) ######################
    docker_utils.rename_container_interface(networks['mec'].ip_range,
                                            networks['mec'].interface,
                                            mec_apps[mec_app].docker_id) ######################
    docker_utils.connect_app_to_host(mec_apps[mec_app],
                                     networks['mec'].interface,
                                     networks['ue'].ip_range) ######################

  events_init = links
  connections = set()
  for event in events_init:
    connections.add((event.ue, event.mec_host))

  for element in connections:
    element[0].add_new_peer(element[1].infra_ip)
    element[1].add_new_peer(element[0].infra_ip)
    docker_utils.start_link(element[0], element[1], networks['infra']) ######################

  
  # Teste de API
  server_app = structures.PythiaServerApp(name='server', image='apps_list:latest', ip=server_ip)
  docker_utils.create_api_container(server_app, networks['ue']) ######################
  docker_utils.start_container(server_app) ######################
"""
def start(mec_hosts, UEs, mec_apps):
  for vmh in mec_hosts:
    docker_utils.start_container(mec_hosts[vmh])

  for vUE in UEs:
    docker_utils.start_container(UEs[vUE])
    for app in UEs[vUE].apps:
      docker_utils.start_container(app)

  for app in mec_apps:
    docker_utils.start_container(mec_apps[app])
"""
def finish(networks, mec_hosts, UEs):
  """This function removes all the containers 
  and networks from docker"""
  for net in networks:
    docker_utils.delete_network(networks[net])

  for vmh in mec_hosts:
    docker_utils.remove_host(mec_hosts[vmh])

  for vUE in UEs:
    docker_utils.remove_host(UEs[vUE])
