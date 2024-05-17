"""This is an example https client.
"""
import requests
import time
import sys
import logging

DELAY = 0.1

logging.basicConfig(level=logging.INFO)

"""if (len(sys.argv) != 4):
  logging.info("Usage: nat_router port destination_ip destination_port")
  logging.info("The url can specify a port http://url:port.")
  logging.info("The delay is measured in seconds.")
  logging.info("The script will request the <url>, repeating every <delay> seconds.")

dport = sys.argv[1]
to_ip = sys.argv[2]
to_port = sys.argv[3]"""

"iptables -A PREROUTING -t nat -p tcp -i eth0 --dport 8001 -j DNAT --to-destination 172.21.0.2:80"
"iptables -A POSTROUTING -t nat -p tcp -d 172.21.0.2 --dport 80 -j MASQUERADE"

"iptables -A PREROUTING -t nat -p udp -i eth0 --dport 8001 -j DNAT --to-destination 172.21.0.2:80"
"iptables -A POSTROUTING -t nat -p udp -d 172.21.0.2 --dport 80 -j MASQUERADE"

"iptables -A PREROUTING -t nat -p tcp -i eth0 --dport 27960 -j DNAT --to-destination 172.21.0.2:27960"
"iptables -A POSTROUTING -t nat -p tcp -d 172.21.0.2 --dport 27960 -j MASQUERADE"

"iptables -A PREROUTING -t nat -p udp -i eth0 --dport 27960 -j DNAT --to-destination 172.21.0.2:27960"
"iptables -A POSTROUTING -t nat -p udp -d 172.21.0.2 --dport 27960 -j MASQUERADE"

logging.info("Starting client")
while(True):
  #logging.info("Running")
  #time.sleep(DELAY)