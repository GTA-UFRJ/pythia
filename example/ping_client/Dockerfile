FROM python:3

RUN apt update -y;
RUN apt install iproute2 -y; apt install iputils-ping -y;

ENTRYPOINT ["ping", "-i", "0.5"]