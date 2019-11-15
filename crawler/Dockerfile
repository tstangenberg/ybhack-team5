FROM alpine
LABEL maintainer="Naresh A."

ENV PYTHONPATH=/

RUN apk --no-cache add python3 py3-cryptography \
    && pip3 install --upgrade pip \
    && pip3 install elasticsearch tweepy --no-cache-dir \
    && adduser -D crawler

COPY crawler/run.py /
RUN python3 -m compileall /run.py

USER crawler
WORKDIR /
CMD [ "python3", "/run.py" ]
