FROM ubuntu:latest

#Autor
MAINTAINER Hugo Barzano Cruz <hugobarzano@gmail.com>
ENV PYTHONUNBUFFERED 1
#Actualizar Sistema Base
RUN sudo apt-get -y update

RUN sudo apt-get -y install mongodb
RUN sudo sed -i 's/^bind_ip = 127.0.0.1/\bind_ip = 0.0.0.0/g' /etc/mongodb.conf
RUN sudo iptables -A INPUT -s 0.0.0.0 -p tcp --destination-port 27017 -m state --state NEW,ESTABLISHED -j ACCEPT"
RUN sudo iptables -A OUTPUT -d 0.0.0.0 -p tcp --source-port 27017 -m state --state ESTABLISHED -j ACCEPT

EXPOSE 27017
