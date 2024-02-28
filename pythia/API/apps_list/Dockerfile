FROM python:3.9.2

WORKDIR /app

RUN pip install requests

RUN pip install Flask

EXPOSE 5000

ENV FLASK_ENV development

COPY app.py .

COPY scenario.xml .

CMD ["flask", "run", "--host", "0.0.0.0"]
