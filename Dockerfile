FROM ubuntu:latest

RUN apt-get update && \
  apt-get install -y python-pip && \
  pip install saws

ENTRYPOINT ["saws"]
