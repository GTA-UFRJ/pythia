#This script starts the application in a g5k host

APK_FILE=edge-client-sample.apk
PACKAGE_NAME='com.example.edgeclientsample'
sudo-g5k
g5k-setup-docker -t
docker build -t edge-server-sample ./server
docker run --name edge-server-container -dp 8080:8080 edge-server-sample
MEC_HOST_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' edge-server-container)
docker run --privileged -d -p 6080:6080 -p 5554:5554 -p 5555:5555 -e DEVICE="Samsung Galaxy S6" --name android-container budtmo/docker-android-x86-8.1
UE_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' android-container)
sudo apt install adb -y
adb connect $UE_IP:5555
adb root
adb connect $UE_IP:5555
adb -s $UE_IP:5555 push $APK_FILE '/data/local/'
adb -s $UE_IP:5555 install $APK_FILE
MEC_HOST_URL="http://${MEC_HOST_IP}:8080"
adb -s $UE_IP:5555 shell am start -n $PACKAGE_NAME/$PACKAGE_NAME.MainActivity -e server_ip $MEC_HOST_URL