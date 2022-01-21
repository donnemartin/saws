FROM python:alpine

ADD . /saws/

RUN cd saws && python setup.py install && cd ..

ENTRYPOINT ["saws"]
