"""This is an example https client.
"""
import sys
import logging
import subprocess

logging.basicConfig(level=logging.INFO)

logging.info("Starting nat_router")


subprocess.call(["iptables", "-A", "PREROUTING", 
"-t", "nat", "-p", "tcp", "-i", "eth0", 
"--dport", "8080", "-j", "DNAT", 
"--to-destination", "172.21.0.2:80"])

subprocess.call(["iptables", "-A", "POSTROUTING", 
"-t", "nat", "-p", "tcp", 
"-d", "172.21.0.2", "--dport", "80", 
"-j", "MASQUERADE"])

subprocess.call(["iptables", "-A", "PREROUTING", 
"-t", "nat", "-p", "tcp", "-i", "eth0", 
"--dport", "27960", "-j", "DNAT", 
"--to-destination", "172.21.0.2:27960"])

subprocess.call(["iptables", "-A", "POSTROUTING",
"-t", "nat", "-p", "tcp",
"-d", "172.21.0.2", "--dport", "27960", 
"-j", "MASQUERADE"])

subprocess.call(["tcpdump", "-v", "-i", "any"])