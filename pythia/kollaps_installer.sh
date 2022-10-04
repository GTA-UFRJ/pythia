#This file sets up kollaps.
#It is meant for g5k terminals, not the frontend.

if [$GRID5000]
then
  g5k-setup-docker -t
fi


# Install Kollaps
git clone --branch master --depth 1 --recurse-submodules $KOLLAPS_REPO
cd Kollaps

export DOCKER_BUILDKIT=1
docker build --rm -f dockerfiles/Kollaps -t kollaps:1.0 .
docker build -f dockerfiles/DeploymentGenerator -t kollaps-deployment-generator:1.0 .

docker swarm init
docker network create --driver=overlay --subnet=10.1.0.0/24 kollaps_network

