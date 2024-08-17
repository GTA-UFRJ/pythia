docker stop $(docker ps -a -q);docker rm $(docker ps -a -q)
docker network rm mec_network ue_network infra_network
docker swarm leave --force