FROM python:3

ADD ./detect_latency.py /

RUN apt update
RUN apt install iproute2 -y; apt install iputils-ping -y
RUN pip3 install requests

ENTRYPOINT ["python3", "/detect_latency.py"]
CMD ["172.21.0.3"]
