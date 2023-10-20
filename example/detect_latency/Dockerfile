FROM python:3

ADD ./detect_latency.py /

RUN apt update
RUN apt install iproute2 -y; apt install iputils-ping -y
RUN pip3 install requests

CMD ["./detect_latency.py", "172.210.3"]
ENTRYPOINT ["python3"]
