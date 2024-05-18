FROM python:3

ADD ./nat_router.py /

RUN apt update
RUN apt install iproute2 -y; apt install iputils-ping -y; apt install iptables -y; apt install tcpdump -y

RUN pip3 install requests

CMD ["/nat_router.py", "http://172.21.0.3:8080", "1"]
ENTRYPOINT ["python3", "/nat_router.py"]