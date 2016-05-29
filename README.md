#NO-INVENTORY

##Trabajo de Fin de Grado - Programa Becas Talentum StartUP

############################################################################

[![Build Status](https://travis-ci.org/hugobarzano/NoInventory.svg?branch=master)](https://travis-ci.org/hugobarzano/NoInventory)
[![Build Status](https://snap-ci.com/hugobarzano/NoInventory/branch/master/build_image)](https://snap-ci.com/hugobarzano/NoInventory/branch/master)
[![Heroku](https://www.herokucdn.com/deploy/button.png)](http://noinventory.herokuapp.com/)
[![DockerHub](https://www.dropbox.com/s/fl5hrbbjm4g2jec/docker_l.png?dl=1)](https://hub.docker.com/r/hugobarzano/)
[![Azure](https://www.dropbox.com/s/oqur6k70poyscxj/azure.png?dl=1)](http://noinventory.cloudapp.net/)
[![No-Inventory-Android-apk](https://www.dropbox.com/s/xx672e199qvvwgb/android.jpg?dl=1)](https://www.dropbox.com/s/itzz91qe5lw1pew/app-debug.apk?dl=1)

############################################################################


###Descripción

No-Inventory es un sistema alojado en la nube para la gestión de inventarios o almacén.
El sistema permite registrar nuevos elementos en función de las preferencias de cada usuario. Dichos elementos se pueden agrupar en colecciones denominadas catálogos, con el objetivo de mantener el orden en el almacén y llevar el control del estado del inventario.

No-Inventory proporciona un entorno colaborativo que permite trabajar a distintos usuarios agrupados por organizaciones. El sistema genera la información necesaria para identificar de manera única cada elemento y mediante su extensión android, tiene soporte para realizar las tareas de gestión mediante códigos de barras, códigos QR o etiquetas NFC. El objetivo principal de complementar la plataforma web con tecnologías móviles es optimizar y minimizar el tiempo y dinero que conllevan las tareas básicas de inventariado.  


Blog: [http://no-inventory.es/](http://no-inventory.es/)

Twiiter: [@no_inventory](https://twitter.com/no_inventory)

Contacto: hugobarzano@gmail.com

[![Licencia](https://www.dropbox.com/s/o9w70i4i2wfjs9e/gplv3-127x51.png?dl=1)](https://github.com/hugobarzano/NoInventory/blob/master/LICENSE)
###Plataforma Web

La plataforma web esta desarrollada sobre Django, el framework de alto nivel y open source de Python. El modelo de datos esta basado en clases python que interactúan con la base de datos mongoDB, externa el framework mediante el cliente Pymongo. Esto se traduce en un incremento de eficiencia y en el aprovechamiento de la libertad y flexibilidad que otorgan las bases de datos NO-SQL

Para mejorar la experiencia del usuario dentro de la plataforma web, se utilizan técnicas de programación en Fron-End basadas en Ajax, Javascript y Jquery.

La plataforma web utiliza API-REST de Google para generar los códigos QR y los códigos de barras dinámicamente.  La plataforma web cuenta con el potente editor en tiempo real “NiceEditor” para el proceso de generación y edición de informes.  La plataforma utiliza la librería Javascript “Highcharts” para la generación de gráficos. La plataforma utiliza el paquete “Pisa” para exportar informes e identificadores a formato PDF.

La plataforma utiliza el modulo “django-registration-redux” que garantiza la seguridad y la autenticación de usuarios, tanto para la plataforma web como para la extensión Android.

La plataforma utiliza el cliente de mensajería Send-Grid para mostrar el buzón de incidencias en la pagina principal. Esto permite que los usuarios puedan contactar con el administrador en caso de algún problema o contactar con las distintas organizaciones que utilizan el sistema.

###Infraestructura

El sistema cuenta con diversoso tipos de infraestrutura.

  PaaS: Heroku

  IaaS: Azure

  Infraestructura basada en docker

  Infraestructura basada en docker con composicion de Servicios

  Infraestructura basada en herramientas de configuración para entornos virtuales de desarrollo web

    - Vagrant
    - Ansible

  Para consegir esto, se ha utilizado MLab, servicio de base de datos en la nube completamente gestionado que aloja bases de datos MongoDB. MLab se ejecuta en proveedores de la nube de Amazon, Google y Microsoft Azure.

###Aplicación Android
La aplicación Android se encuentra alojada en el repositorio [NoInventory-Android-Apps] (https://github.com/hugobarzano/NoInventory-Android-Apps/tree/master/Noinventory)
Esta extensión de la plataforma es la encargada de la tareas de clasificación. Permite leer/escribir los codigos de barras, codigos qr o etiquetas nfc que identifican a los objetos.
Puede descargarse desde aquí.

  [![No-Inventory-Android-apk](https://www.dropbox.com/s/xx672e199qvvwgb/android.jpg?dl=1)](https://www.dropbox.com/s/itzz91qe5lw1pew/app-debug.apk?dl=1)


###Documentación

La documentación del proyecto se encuentra en este [directorio](https://github.com/hugobarzano/NoInventory/tree/master/NoInventoryDOC). Se está realizando con LaTEX y puede descargarse aquí.

  [No-Inventory-DOC](https://www.dropbox.com/s/4tt3viylmf32la2/proyecto.pdf?dl=1)


### Instalación Local

  [Instalación Local de la aplicación](https://github.com/hugobarzano/NoInventory/blob/master/documentacion/instalacion.md)

###Despliegues

Los distintos despliegues se pueden realizar con la herramienta de construcción [Makefile](https://github.com/hugobarzano/NoInventory/blob/master/makefile) o con el archivo [Vagrant](https://github.com/hugobarzano/NoInventory/blob/master/Vagrantfile) para configuración de entornos de desarrollo virtuales:

    - make heroku

    - make docker

    - make docker_compose

    - vagrant up --provider=azure

### Desarrollo Basado en TDD

Test Propios:

    - [Test Clasificación](https://github.com/hugobarzano/NoInventory/blob/master/NoInventory/test_clasificacion.py)

    - [Test Item](https://github.com/hugobarzano/NoInventory/blob/master/NoInventory/test_item.py)

    - [Test Catálogo](https://github.com/hugobarzano/NoInventory/blob/master/NoInventory/test_catalogo.py)

    - [Test Informe](https://github.com/hugobarzano/NoInventory/blob/master/NoInventory/test_informe.py)

Test Django:

    - [Test.py](https://github.com/hugobarzano/NoInventory/blob/master/NoInventory/tests.py)

Test Navegación:

    - [Test con Selenium](https://github.com/hugobarzano/NoInventory/tree/master/Selenium)

####NinjaMock
[Diseño de la web](https://ninjamock.com/s/KDGZS)
[Diseño de la aplicacion](https://ninjamock.com/s/F12ZS)

###Presentaciónes

[Hackaton Marzo](https://www.dropbox.com/s/2z3nephfqtxzdzc/NO-INVENTORY.pdf?dl=1)

[Hackaton Mayo](https://www.dropbox.com/s/mj4tplyahtk6kxt/Presentacion_hackaton_mayo.pdf?dl=1)
