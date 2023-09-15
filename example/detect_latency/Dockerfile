FROM python:3

ADD ./detect_latency.py /

RUN apt install iputils-ping -y
RUN pip3 install requests

CMD ["./detect_latency.py"]
ENTRYPOINT ["python3"]
