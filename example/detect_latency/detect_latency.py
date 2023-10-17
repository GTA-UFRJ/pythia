import subprocess
import time
import sys

# Definiton of our host IP
host = sys.argv[1]
# Set the amount of time the program will run for
start_time = time.time()
time_elapsed = 0
time_limit = 600

def detect_latency(host):
    try:
        # Run the ping command with a single ping and capture the output. 
        result = subprocess.run(["ping", "-c", "1", host],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # "-c" is the argument for Linux and Android. For this to work in Windows,
        # change it to "-n"
        # Parse the output to extract the minimum, maximum and average round-trip time (RTT)
        lines = result.stdout.splitlines()
        rtt_line = lines[-1]  # Assuming the last line contains RTT information
        return rtt_line
    except subprocess.CalledProcessError:
        # This handles the case where the ping command fails (e.g., host is unreachable)
        return None


# Creation of output file
with open("output/output_file.txt", "a") as output_file:
    while time_elapsed <= time_limit:
        latency = detect_latency(host)
        if latency is not None:
            print(f"Latency to {host}: {latency}")
            output_file.write(f"Latency to {host}: {latency}")
        else:
            print(f"Unable to detect latency to {host}")
            output_file.write(f"Unable to detect latency to {host}")
        # Execute the function every 5 seconds (half the period)  
        time.sleep(5)
        time_elapsed = time.time() - start_time
