docker build -f pythia/images/vmec_host/Dockerfile -t pythia:vmec_host pythia/images/vmec_host
docker build -f pythia/images/vUE/Dockerfile -t pythia:vUE pythia/images/vUE
docker build -f example/simple_server/Dockerfile -t simple_server:latest example/simple_server
docker build -f example/simple_client/Dockerfile -t simple_client:latest example/simple_client
docker build -f example/nat_router/Dockerfile -t nat_router:latest example/nat_router
docker build -f pythia/API/apps_list/Dockerfile -t apps_list:latest pythia/API/apps_list
docker build -f example/detect_latency/Dockerfile -t detect_latency:latest example/detect_latency
docker build -f example/quakejs-docker/Dockerfile -t pythiademo/quakejs example/quakejs-docker