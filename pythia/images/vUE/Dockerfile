FROM debian

RUN apt update -y; apt install iptables -y; apt install iproute2 -y; apt install iputils-ping -y; apt install tcpdump -y; apt install curl -y; apt install python3-pip -y; pip3 install pynetem;
ADD ./forward.sh /

#ENTRYPOINT ["/bin/bash", "/forward.sh"]
ENTRYPOINT ["tcpdump", "-v", "-i", "any"]
