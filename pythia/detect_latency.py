import subprocess
import time
def detect_latency(host):
    try:
        # Run the ping command with a single ping and capture the output
        result = subprocess.run(["ping", "-c", "1", host],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Parse the output to extract the round-trip time (RTT)
        lines = result.stdout.splitlines()
        rtt_line = lines[-1]  # Assuming the last line contains RTT information
        return rtt_line
    except subprocess.CalledProcessError:
        # Handle the case where the ping command fails (e.g., host is unreachable)
        return None

host = "www.ufrj.br"
start_time = time.time()
time_elapsed = 0
time_limit = 300
while time_elapsed <= time_limit:
    latency = detect_latency(host)
    if latency is not None:
        print(f"Latency to {host}: {latency} ms")
    else:
        print(f"Unable to detect latency to {host}")
    time.sleep(10 - (time.time() - start_time) % 10)
    time_elapsed = time.time() - start_time

