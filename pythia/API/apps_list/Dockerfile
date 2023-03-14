FROM python:3.9.2

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_ENV development

COPY app.py .

COPY scenario.xml .

CMD ["flask", "run", "--host", "0.0.0.0"]
