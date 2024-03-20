import subprocess
import time
import sys
from datetime import datetime


time.sleep(5)
# Definiton of our host IP
host = sys.argv[1]
# Set the amount of time the program will run for
startTime = time.time()
timeElapsed = 0
timeLimit = 50

def DetectLatency(host):
    timeOfRequest = datetime.now()
    timeOfRequest = timeOfRequest.strftime("%H:%M:%S.%f")[:-3]
    try:
        # Run the ping command with a single ping and capture the output. 
        result = subprocess.run(["ping", "-c", "1", host],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # "-c" is the argument for Linux and Android. For this to work in Windows,
        # change it to "-n"
        # Parse the output to extract the minimum, maximum and average round-trip time (RTT)
        lines = result.stdout.splitlines()
        # Assuming the last element contains RTT data
        rttLine = lines[-1]
        # Since it's a single request, minimum, maximum and average round-trip time are all the same,
        # so we can pick one
        rttLine = rttLine.split("/")[4]
        return rttLine, timeOfRequest
    except subprocess.CalledProcessError:
        # This handles the case where the ping command fails (e.g., host is unreachable)
        return None, timeOfRequest


# Creation of output file
with open("output/output_file.txt", "a") as output_file:
    while timeElapsed <= timeLimit:
        latency, currentTime = DetectLatency(host)
        if latency is not None:
            output_file.write(f"{currentTime} - Latency to {host}: {latency}\n")
            output_file.flush()
        else:
            output_file.write(f"{currentTime} - Unable to detect latency to {host}\n")
            output_file.flush()
        # Execute the function every 5 seconds (half the period)  
        time.sleep(5)
        timeElapsed = time.time() - startTime
