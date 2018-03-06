FROM python:3.5-alpine

ARG HATSTALL_VERSION

ENV HATSTALL_GUNICORN_WORKERS=2
ENV HATSTALL_GUNICORN_TIMEOUT=90

EXPOSE 8001

LABEL \
  maintainer="Chaoss" \
  description="Hatstall is a web interface for SortingHat databases developed mainly with Django" \
  project="https://github.com/chaoss/grimoirelab-hatstall.git" \
  version="$HATSTALL_VERSION"

RUN \
  addgroup -g 1000 hatstall && \
  adduser -u 1000 -G hatstall -h /hatstall -D hatstall

COPY --chown=hatstall ./django_hatstall /hatstall
COPY --chown=hatstall ./requirements.txt /hatstall/requirements.txt
COPY --chown=hatstall ./docker/alpine/entrypoint.sh /hatstall/entrypoint.sh

RUN \
  chmod +x /hatstall/entrypoint.sh && \
  apk add --no-cache tini gcc g++ musl-dev freetype freetype-dev && \
  pip3 install --no-cache --upgrade pip && \
  pip3 install --no-cache cython gunicorn

USER hatstall

WORKDIR /hatstall

RUN \
  pip3 install --user --no-cache -r requirements.txt && \
  mkdir /hatstall/staticfiles

ENTRYPOINT ["/sbin/tini","--","/hatstall/entrypoint.sh"]
