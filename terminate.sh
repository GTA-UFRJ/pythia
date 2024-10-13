# Stop and remove all containers
containers=$(docker ps -aq)
if [ -n "$containers" ]; then
  docker stop $containers
  docker rm $containers
fi

# Leaves the docker swarm
# docker info | grep -q "Swarm: active" && docker swarm leave --force
docker swarm leave --force

# Remove the following networks if they exist
for network in mec_network ue_network infra_network ingress docker_gwbridge; do
  if docker network inspect $network >/dev/null 2>&1; then
    docker network rm $network
  fi
done