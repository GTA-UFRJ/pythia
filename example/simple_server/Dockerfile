FROM python:3

ADD ./simple_server.py /

RUN apt update
RUN apt install iproute2 -y; apt install iputils-ping -y

CMD ["/simple_server.py", "8080"]
ENTRYPOINT ["python3"]
