"""This file runs the emulation stage of Pythia"""


"""TODO:
Emulation must create UEApp, vUE, and vMEC containers.
The MEC Platform should be responsible for MECApp creation"""

import pythia.docker_utils as docker_utils
import logging
import sys
import time

logging.basicConfig(level=logging.INFO)

def emulate(networks, links):
  """This function runs the emulation phase of Pythia"""

  #Create emulation events queue
  events_queue = links
  events_queue.sort(key=lambda x: x.time, reverse=True)
  
  emulation_zero = time.time()
  emulation_time_error = 0.3
  event = events_queue.pop()
  #Start main emulation loop
  while(len(events_queue)):
    emulation_time = time.time() - emulation_zero
    time_difference = event.time - emulation_time
    if time_difference < emulation_time_error:
      for ue_app in event.ue.apps:
        for mec_app in event.mec_host.active_apps:
          docker_utils.change_link(ue_app, mec_app,
                             networks['ue'], networks['mec'],
                           event.upload, event.latency)
      event = events_queue.pop()
      time_difference = event.time - emulation_time
    logging.info(f"Event time = {event.time}, emu time = {emulation_time}, Time diff = {time_difference}")
    if time_difference < 0:
      continue
    time.sleep(time_difference)
    print(f"Event = {event}")

def bootstrap(networks, mec_hosts, mec_apps, UEs):
  # Need to create the ping_sender and ping_receiver containers.
  """This function bootstraps the emulation.
  It creates the emulation scenario inside docker, 
  with UEs and MECHosts, their networks and ips."""

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
    docker_utils.create_host(mec_hosts[vmh],
                             networks['infra'],
                             networks['mec'])
    docker_utils.start_container(mec_hosts[vmh])

  #Create UEs
  for vUE in UEs:
    UEs[vUE].infra_ip = networks['infra'].allocate_ip()
    UEs[vUE].external_ip = networks['ue'].allocate_ip()
    docker_utils.create_host(UEs[vUE],
                             networks['infra'],
                             networks['ue'])
    docker_utils.start_container(UEs[vUE])

    #Start apps on each vUE
    #TODO: Set this on emulation start
    for ue_app in UEs[vUE].apps:
      ue_app.ip = networks['ue'].allocate_ip()
      ue_app.host = UEs[vUE]
      docker_utils.create_external_app(ue_app, networks['ue'])
      docker_utils.start_container(ue_app)
      docker_utils.connect_app_to_host(ue_app)

  #Start MEC apps. Allocate them to first host
  #Todo: start MEC Apps through MEC System.
  mec_host = mec_hosts[list(mec_hosts.keys())[0]]
  for mec_app in mec_apps:
    mec_apps[mec_app].host = mec_host
    mec_host.active_apps.add(mec_apps[mec_app])
    docker_utils.create_mec_app(mec_apps[mec_app], networks['mec'])

    #Set route to this mec_app
    for vUE in UEs:
      for ue_app in UEs[vUE].apps:
        docker_utils.connect_app_to_app(ue_app, mec_apps[mec_app])

    #Isso deveria estar aqui??
    docker_utils.start_container(mec_apps[mec_app])
    docker_utils.connect_app_to_host(mec_apps[mec_app])

  #Testing netem:
  #TODO: change this
  ue_app = UEs[list(UEs.keys())[0]].apps[0]
  mec_app = mec_apps[list(mec_apps.keys())[0]]
  docker_utils.change_link(ue_app, mec_app,
                           networks['ue'], networks['mec'],
                           5000, 500, 10)

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
