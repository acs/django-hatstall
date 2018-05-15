# Copyright (C) 2018 Bitergia
# GPLv3 License

FROM debian:stretch-slim

ARG HATSTALL_VERSION

LABEL \
  maintainer="Alvaro del Castillo <acs@bitergia.com>" \
  description="Hatstall is a web interface to manage sortinghat database" \
  project="https://github.com/chaoss/grimoirelab-hatstall" \
  version="$HATSTALL_VERSION"

EXPOSE 80

ENV DEBIAN_FRONTEND noninteractive
ENV DEPLOY_USER www-data
ENV DEPLOY_USER_DIR /var/www

ENV HATSTALL_ADMIN_USER admin
ENV HATSTALL_ADMIN_MAIL admin@example.com
ENV HATSTALL_ADMIN_PASS admin
ENV HATSTALL_ALLOWED_HOST '[]'
ENV HATSTALL_DATABASE /var/www/hatstall.sqlite3
ENV HATSTALL_DEBUG False

ADD https://github.com/krallin/tini/releases/download/v0.18.0/tini /sbin/tini

# install dependencies
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        bash locales \
        gcc \
        git git-core \
        mysql-client \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        unzip curl wget sudo ssh vim \
        apache2 libapache2-mod-wsgi-py3 ssl-cert \
        && \
    apt-get clean && \
    find /var/lib/apt/lists -type f -delete && \
    chmod 0755 /sbin/tini

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN \
  sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  echo 'LANG="en_US.UTF-8"'>/etc/default/locale && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8

# Install pip packages needed
RUN \
  pip3 install --no-cache-dir django wheel && \
  pip3 install --no-cache-dir python-dateutil && \
  pip3 install --no-cache-dir pandas==0.18.1 && \
  pip3 install --no-cache-dir setuptools && \
  pip3 install --no-cache-dir sortinghat

COPY django-hatstall ${DEPLOY_USER_DIR}/django-hatstall

COPY docker/apache-hatstall.conf /etc/apache2/sites-available/000-default.conf
COPY docker/apache-hatstall.conf /etc/apache2/sites-enabled/000-default.conf

ADD docker/stage /entrypoint
RUN chmod 755 /entrypoint

WORKDIR ${DEPLOY_USER_DIR}

ENTRYPOINT [\
  "/sbin/tini", "--",\
  "/bin/sh", "-c", \
  "/entrypoint"\
  ]
