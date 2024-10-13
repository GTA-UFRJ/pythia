#!/bin/bash

# Define the path to the Docker daemon configuration file
DAEMON_JSON="/etc/docker/daemon.json"
BACKUP_JSON="/etc/docker/daemon.json.bak"
DOCKER_SERVICE_FILE="/lib/systemd/system/docker.service"

# Function to check if the Docker Engine API is already activated
is_activated() {
  if sudo grep -q '"tcp://0.0.0.0:2375"' $DAEMON_JSON; then
    return 0
  else
    return 1
  fi
}

# Function to remove the -H fd:// flag from the docker.service file
remove_fd_flag() {
  if sudo grep -q ' -H fd://' $DOCKER_SERVICE_FILE; then
    sudo sed -i 's/ -H fd:\/\///g' $DOCKER_SERVICE_FILE
    sudo systemctl daemon-reload
  fi
}

# Function to activate the Docker Engine API
activate_api() {
  # Backup the original daemon.json file if it doesn't exist
  if [ ! -f "$BACKUP_JSON" ]; then
    sudo cp $DAEMON_JSON $BACKUP_JSON
  fi

  # Update the daemon.json to enable the Docker Engine API over TCP
  sudo tee $DAEMON_JSON > /dev/null <<EOL
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"]
}
EOL

  # Remove the -H fd:// flag from the docker.service file
  remove_fd_flag

  # Restart the Docker service to apply the changes
  if ! sudo systemctl restart docker; then
    echo "Failed to restart Docker service. Please check the configuration and logs."
    echo "Use 'systemctl status docker.service' and 'journalctl -xeu docker.service' for details."
    sudo systemctl status docker.service
    sudo journalctl -u docker.service -n 50
    exit 1
  fi

  # Verify the Docker daemon is listening on the TCP port
  echo "Verifying the Docker daemon is listening on port 2375..."
  sudo netstat -tuln | grep 2375

  echo "Docker Engine API has been activated."
}

# Main script logic
if is_activated; then
  echo "Docker Engine API is already activated."
else
  activate_api
fi

