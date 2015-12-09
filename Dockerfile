FROM ubuntu:latest

RUN apt-get update groff && \
  apt-get install -y python-pip && \
  pip install saws

ENTRYPOINT ["saws"]
