import subprocess
import time
import sys


time.sleep(1)
# Definiton of our host IP
host = sys.argv[1]
# Set the amount of time the program will run for
startTime = time.time()
timeElapsed = 0
timeLimit = 50

def DetectLatency(host):
    timeOfRequest = time.localtime()
    timeOfRequest = time.strftime("%H:%M:%S", timeOfRequest)
    try:
        # Run the ping command with a single ping and capture the output. 
        result = subprocess.run(["ping", "-c", "1", host],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # "-c" is the argument for Linux and Android. For this to work in Windows,
        # change it to "-n"
        # Parse the output to extract the minimum, maximum and average round-trip time (RTT)
        lines = result.stdout.splitlines()
        rttLine = lines
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
        else:
            output_file.write(f"{currentTime} - Unable to detect latency to {host}\n")
        # Execute the function every 5 seconds (half the period)  
        time.sleep(5)
        timeElapsed = time.time() - startTime
