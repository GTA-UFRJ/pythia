# Stop and remove all running containers
running_containers=$(docker ps -q)
if [ -n "$running_containers" ]; then
  docker stop $running_containers
  docker rm $running_containers
fi

# Leaves the docker swarm
docker info | grep -q "Swarm: active" && docker swarm leave --force

# Remove the following networks if they exist
for network in mec_network ue_network infra_network ingress docker_gwbridge; do
  if docker network inspect $network >/dev/null 2>&1; then
    docker network rm $network
  fi
done