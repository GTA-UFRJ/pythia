"""This file takes care of the life cycle
of Pythia experiment"""
import configparser
import sys
import os
import argparse
from pythia import emulation, structures, xml_parser
import docker

configuration_file = 'pythia.ini'

# Preparing command line arguments
parser = argparse.ArgumentParser(description="Pythia, a MEC mobility emulator.")
parser.add_argument('-config', 
  help=f"Path to the configuration file. Defaults to {configuration_file}.")

args = parser.parse_args()

if args.config:
  configuration_file = args.config

#Read configuration file
#The configuration file has explanations about each variable
config = configparser.ConfigParser()
config.read(configuration_file)
scenario_filename = config['EXPERIMENT']['experiment_descriptor']

default_latency = config['DEFAULT']['default_radio_latency']
default_download = config['DEFAULT']['default_radio_download']
default_upload = config['DEFAULT']['default_radio_upload']
mec_hosts_image = config['DEFAULT']['mec_host_image']
mec_host_command = "" if not config.has_option('DEFAULT','mec_host_command') \
             else config['DEFAULT']['mec_host_command']
#Friends don't let friends use ternary operator
ue_image = config['DEFAULT']['ue_image']
ue_command = "" if not config.has_option('DEFAULT','ue_command') \
             else config['DEFAULT']['ue_command']

mec_network_name = config['DEFAULT']['mec_network_name']
mec_network_range = config['DEFAULT']['mec_network_range']
mec_network_interface = config['DEFAULT']['mec_network_interface']

ue_network_name = config['DEFAULT']['ue_network_name']
ue_network_range = config['DEFAULT']['ue_network_range']
ue_network_interface = config['DEFAULT']['ue_network_interface']

infra_network_name = config['DEFAULT']['infra_network_name']
infra_network_range = config['DEFAULT']['infra_network_range']
infra_network_interface = config['DEFAULT']['infra_network_interface']
server_ip = config['DEFAULT']['server_ip']

networks = {}
networks['mec'] = structures.PythiaNetwork(mec_network_name,
                                                mec_network_range,
                                                mec_network_interface)

networks['ue'] = structures.PythiaNetwork(ue_network_name,
                                                ue_network_range,
                                                ue_network_interface)

networks['infra'] = structures.PythiaNetwork(infra_network_name,
                                                infra_network_range,
                                                infra_network_interface)

#Read experiment file
mec_hosts, UEs, mec_apps, links = \
  xml_parser.parse_scenario(scenario_filename)

#Setting hosts images
for mec_h in mec_hosts:
  mec_hosts[mec_h].image = mec_hosts_image

for ue in UEs:
  UEs[ue].image = ue_image

#Invoke link estimation
"""UEs = estimation.estimate(mec_hosts,
                          UEs,
                          base_stations,
                          default_latency,
                          default_download,
                          default_upload)"""

#Bootstrap emulation
emulation.bootstrap(networks, mec_hosts, mec_apps,UEs, links, server_ip)

#Invoke emulation
emulation.emulate(networks, links)

#Terminate all running containers
os.system("./terminate.sh")
