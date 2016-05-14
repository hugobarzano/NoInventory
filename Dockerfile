FROM ubuntu:latest

#Autor
MAINTAINER Hugo Barzano Cruz <hugobarzano@gmail.com>
ENV PYTHONUNBUFFERED 1
#Actualizar Sistema Base
RUN sudo apt-get -y update

#Descargar aplicacion
RUN sudo apt-get install -y git
RUN sudo git clone https://github.com/hugobarzano/NoInventory.git

# Instalar Python y PostgreSQL
RUN sudo apt-get install -y python-setuptools
RUN sudo apt-get -y install python-dev
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install libpq-dev
RUN sudo apt-get -y install mongodb
RUN sudo apt-get -y install python-reportlab
RUN sudo easy_install pip
RUN sudo pip install --upgrade pip
RUN sudo python -m pip install pymongo==2.8



#Instalamos la aplicacion
RUN ls
RUN cd NoInventory/ && ls -l
RUN cd NoInventory/ && sudo pip install -r requirements.txt
