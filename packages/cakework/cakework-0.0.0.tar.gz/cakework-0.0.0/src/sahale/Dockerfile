# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 50051
CMD ["python3", "activity_server.py"]
