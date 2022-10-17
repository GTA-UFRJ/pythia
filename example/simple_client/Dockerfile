FROM python:3

ADD ./simple_client.py /

RUN apt update
RUN apt install iproute2 -y; apt install iputils-ping -y

RUN pip3 install requests

CMD ["/simple_client.py", "http://172.21.0.3:8080", "1"]
ENTRYPOINT ["python3"]