FROM alpine
LABEL maintainer="Naresh A."

ENV PYTHONPATH=/

RUN apk --no-cache add python3 py3-cryptography \
    && pip3 install --upgrade pip \
    && pip3 install textblob elasticsearch tweepy --no-cache-dir \
    && adduser -D crawler

COPY importer.py /
RUN python3 -m compileall /importer.py

USER crawler
WORKDIR /
CMD [ "python3", "/importer.py" ]
