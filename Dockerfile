FROM ubuntu:latest

RUN apt-get update && \
  apt-get install -y python-pip groff && \
  pip install saws

ENTRYPOINT ["saws"]
