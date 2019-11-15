FROM alpine
LABEL maintainer="Daniel S."

ENV PYTHONPATH=/app

RUN apk --no-cache add python3 py3-cryptography \
    && pip3 install --upgrade pip \
    && pip3 install flask elasticsearch flake8 --no-cache-dir \
    && adduser -D web

COPY frontend/app /app
RUN chown -R web /app/ \
    && flake8 /app/run.py \
    && python3 -m compileall /app/*.py

USER web
WORKDIR /app
CMD [ "python3", "/app/run.py" ]

