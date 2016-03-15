FROM ubuntu:latest

#Autor
MAINTAINER Hugo Barzano Cruz <hugobarzano@gmail.com>
ENV PYTHONUNBUFFERED 1
#Actualizar Sistema Base
RUN sudo apt-get -y update

RUN sudo apt-get -y install mongodb
RUN sudo sed -i 's/^ bind_ip = 127.0.0.1/ bind_ip = 0.0.0.0/g' /etc/mongod.conf



#Instalamos la aplicacion
RUN ls
RUN cd NoInventory/ && ls -l
RUN cd NoInventory/ && sudo pip install -r requirements.txt
