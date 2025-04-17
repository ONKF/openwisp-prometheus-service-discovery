FROM alpine:3.21.3

WORKDIR /opt/openwisp-prometheus-service-discovery

COPY environment.txt .

RUN apk add --no-cache uwsgi-python3 python3 py3-pip && pip3 install --no-cache-dir -r environment.txt --break-system-packages

COPY main.py .

ENTRYPOINT /usr/sbin/uwsgi --socket 0.0.0.0:8080 --uid uwsgi --plugins python3 --protocol http --wsgi main:app