"""This is an example https client.
"""
import requests
import time
import sys
import logging

logging.basicConfig(level=logging.INFO)

if (len(sys.argv) != 3):
  logging.info("Usage: python url delay")
  logging.info("The url can specify a port http://url:port.")
  logging.info("The delay is measured in seconds.")
  logging.info("The script will request the <url>, repeating every <delay> seconds.")

url = sys.argv[1]
delay = int(sys.argv[2])
print(f"Requesting {url} every {delay}s.")

logging.info("Starting client")
while(True):
  try:
    r = requests.get(url)
    logging.info(r.text)
  except:
    logging.info("Something went wrong, we will try again.")

  time.sleep(delay)