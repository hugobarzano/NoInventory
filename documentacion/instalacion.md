#Instalación

##Intalación Local

Para instalar la aplicación en nuestro ordenador será necesario clonar el repositorio y ejecutar:

  make install

Esta acción realizará las siguientes tareas:

        #!/bin/bash

        #Actualizar Sistema Base
        echo "actualizar sistema base"
        sudo apt-get -y update

        # Instalacion
        echo "Instalar dependencias"
        sudo apt-get -y install git
        sudo apt-get -y install python-setuptools
        sudo apt-get -y install python-dev
        sudo apt-get -y install build-essential
        sudo apt-get -y install libpq-dev
        sudo apt-get -y install mongodb
        sudo easy_install pip
        sudo pip install --upgrade pip
        sudo python -m pip install pymongo==3.1.1
        #Instalamos requisitos
        echo "instalar requirements"
        sudo pip install -r requirements.txt
