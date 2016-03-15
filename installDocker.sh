#!/bin/bash
  sudo -i apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-key$
	sudo -i echo /etc/apt/sources.list.d/docker.list deb https://apt.dockerproject.$
	sudo -i apt-get update
	#sudo -i apt-cache policy docker-engine
	#sudo -i apt-get -y install linux-image-extra-$(uname -r)
	#sudo -i apt-get -y install linux-image-generic-lts-trusty
	sudo -i apt-get -y install curl
	curl -sSL https://get.docker.com/gpg | sudo apt-key add -
	curl -sSL https://get.docker.com/ | sh
	sudo -i apt-get -y install python-pip
	sudo -i pip install docker-compose
