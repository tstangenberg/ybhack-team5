FROM alpine
LABEL maintainer="Naresh A."

ENV PYTHONPATH=/app

RUN apk --no-cache add python3 py3-cryptography \
    && pip3 install --upgrade pip \
    && pip3 install elasticsearch tweepy --no-cache-dir \
    && adduser -D crawler

COPY crawler/run.py /app
RUN chown -R crawler /app/ \
    #&& flake8 /app/run.py \
    && python3 -m compileall /app/*.py

USER crawler
WORKDIR /app
CMD [ "python3", "/app/run.py" ]
