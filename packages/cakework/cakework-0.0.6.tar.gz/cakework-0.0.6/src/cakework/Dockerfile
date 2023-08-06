# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# COPY ./requirements_cakework.txt /app/requirements_cakework.txt
WORKDIR /app
# don't want to install cakework twice
RUN pip3 install grpcio protobuf cakework
COPY . /app
RUN pip3 install -r requirements.txt
ENV MODULE=submodule.activity 
ENV ACTIVITY=activity
EXPOSE 50051
CMD ["python3", "-m", "cakework.activity_server"]