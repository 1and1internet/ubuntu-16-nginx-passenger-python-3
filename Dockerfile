FROM 1and1internet/ubuntu-16-nginx-passenger
MAINTAINER brian.wilkinson@1and1.co.uk
ARG DEBIAN_FRONTEND=noninteractive

ENV VIRTENV /var/www/._venv
ENV VIRTUAL_ENV_DISABLE_PROMPT true
ENV PATH $VIRTENV/bin:$PATH

RUN \
	apt-get update -q && \
	apt-get install -q -o Dpkg::Options::=--force-confdef -y virtualenv python3-venv python3-virtualenv python3-all python3-setuptools python3-pip && \
	apt-get install -q -o Dpkg::Options::=--force-confdef -y python-dev python3-dev python-pip && \
	pip install requests logging && \
	/usr/bin/pyvenv ${VIRTENV}/ && \
	/bin/bash -c " \
		source ${VIRTENV}/bin/activate && \
		python --version && \
		pip --version && \
		pip install --no-cache-dir --upgrade pip && \
		pip install --no-cache-dir mysqlclient && \
		pip install --no-cache-dir flask \
	" && \
	chmod -R 777 $VIRTENV && \
	echo "passenger_python ${VIRTENV}/bin/python3;" >> /etc/nginx/passenger.conf && \
	/usr/bin/passenger-config validate-install  --auto --no-colors && \
  apt-get -y clean && \
  rm -rf /var/lib/apt/lists/*

COPY src /var/www/
EXPOSE 8080 8443
WORKDIR /var/www

