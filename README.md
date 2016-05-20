#NO-INVENTORY

##Trabajo de Fin de Grado - Programa Becas Talentum StartUP

############################################################################

[![Build Status](https://travis-ci.org/hugobarzano/NoInventory.svg?branch=master)](https://travis-ci.org/hugobarzano/NoInventory)
[![DockerHub](https://www.dropbox.com/s/fl5hrbbjm4g2jec/docker_l.png?dl=1)](https://hub.docker.com/r/hugobarzano/)
[![Azure](https://www.dropbox.com/s/oqur6k70poyscxj/azure.png?dl=1)](http://noinventory.cloudapp.net/)

############################################################################


###Descripción

No-Inventory es un sistema alojado en la nube para la gestión de inventarios o almacén.
El sistema permite registrar nuevos elementos en función de las preferencias de cada usuario. Dichos elementos se pueden agrupar en colecciones denominadas catálogos, con el objetivo de mantener el orden en el almacén y llevar el control del estado del inventario.

No-Inventory proporciona un entorno colaborativo que permite trabajar a distintos usuarios agrupados por organizaciones. El sistema genera la información necesaria para identificar de manera única cada elemento y mediante su extensión android, tiene soporte para realizar las tareas de gestión mediante códigos de barras, códigos QR o etiquetas NFC. El objetivo principal de complementar la plataforma web con tecnologías móviles es optimizar y minimizar el tiempo y dinero que conllevan las tareas básicas de inventariado.  


Blog: [http://no-inventory.es/](http://no-inventory.es/)

Twiiter: [@no_inventory](https://twitter.com/no_inventory)

Contacto: hugobarzano@gmail.com

###Objetivos

[Objetivos](https://github.com/hugobarzano/NoInventory/blob/master/documentacion/objetivos.md) del proyecto, cosas que se quieren hacer, cosas que se han hecho, cosa de interes.  

###Instalación

[Instalación Local de la aplicación](https://github.com/hugobarzano/NoInventory/blob/master/documentacion/instalacion.md)
###Infraestructura

El sistema cuenta con diversoso tipos de infraestrutura.

  Infraestructura basada en docker

  Infraestructura basada en docker con composicion de Servicios

  Infraestructura basada en herramientas de configuración para entornos virtuales de desarrollo web

    - Vagrant
    - Ansible

Todas ellas corriendo sobre azure

Una infraestructura similar, de una rama anteiror del proyecto la podemos encontrar aqui: [osl-computer-management](https://github.com/hugobarzano/osl-computer-management)

###Aplicación Android

La aplicación Android del proyecto se encuentra alojada en el repositorio [NoInventory-Android-Apps] (https://github.com/hugobarzano/NoInventory-Android-Apps)

###Documentación
####NinjaMock
[Diseño de la web](https://ninjamock.com/s/KDGZS)

[Diseño de la aplicacion](https://ninjamock.com/s/F12ZS)

####Casos de uso
[Documento casos de uso](https://www.dropbox.com/s/90tang9wazsx1vt/casos_uso.odt?dl=1)

####Análisis de Requisitos
[Documento requisitos de información](https://www.dropbox.com/s/ipidn2bou6xmexf/requitos.odt?dl)

###Herramientas y cosas utiles

[Investigar 123d](http://www.123dapp.com/catch)
[Realizar Diagramas Online](https://creately.com/app/?tempID=h165rwt81&login_type=demo#)

[Disparadores para redes sociales](https://ifttt.com/recipes)

[POST-TUNELING](https://baxeico.wordpress.com/2014/06/25/put-and-delete-http-requests-with-django-and-jquery/)

###Tutoriales

[Implementar lector codigos](http://code.tutsplus.com/tutorials/android-sdk-create-a-barcode-reader--mobile-17162)
[implementar interfaz](http://www.androidhive.info/2013/11/android-sliding-menu-using-navigation-drawer/)
[NFC](http://www.jessechen.net/blog/how-to-nfc-on-the-android-platform/)
[NFC2](http://www.creativebloq.com/android/getting-started-nfc-android-5122811)
[NFC3](http://androcode.es/2013/04/nfc-i-explicacion-tutorial-basico-y-sorteo/)
[NFC4](http://code.tutsplus.com/tutorials/reading-nfc-tags-with-android--mobile-17278)
[NFC5](http://www.survivingwithandroid.com/2016/01/how-to-write-nfc-tag-in-android-2.html)
[Tutoriales android](http://www.survivingwithandroid.com/category/android-tutorial/page/6)
[boostrap](http://librosweb.es/libro/bootstrap_3/)
[conexion http](https://danielme.com/tip-android-8-obtener-recursos-web/)
[webview](http://www.desarrollolibre.net/blog/tema/152/android/como-mostrar-paginas-web-con-webview-en-android#.VwPR6UKlilM)
[JsonCustonRequest](http://stackoverflow.com/questions/25948191/send-post-request-using-volley-and-receive-in-php)
[draggable and droppable](http://www.desarrolloweb.com/articulos/ejemplo-drag-drop-jquery.html)
[paginacion](http://www.bootply.com/zT2ZU9DSDM#)
[mongo](http://rafinguer.blogspot.com.es/2014/10/fechas-en-mongodb.html)
[instaclik](http://instantclick.io/)
[seleniun](http://docs.seleniumhq.org/)
[twill](http://twill.idyll.org/)
[uml](https://www.gliffy.com/go/html5/10619971#)
[notificaciones](http://pjdietz.com/jquery-plugins/freeow/)
###dDOC
[libro](https://books.google.es/books?id=B6LAqCoPSeoC&pg=PA547&lpg=PA547&dq=%C2%BFcuanto+dinero+gastan+las+empresas+en+realizar+inventario?&source=bl&ots=vO72tajNO_&sig=v0GlPUNV03wV8iuxgUqJVnjX8e4&hl=es&sa=X&ved=0ahUKEwij_7DLtNTMAhXoKJoKHWYhAXMQ6AEIKDAC#v=onepage&q=%C2%BFcuanto%20dinero%20gastan%20las%20empresas%20en%20realizar%20inventario%3F&f=false)
###Presentación Concurso Software libre

[Hackaton Marzo](https://www.dropbox.com/s/2z3nephfqtxzdzc/NO-INVENTORY.pdf?dl=1)
[editor](https://scotch.io/tutorials/building-a-real-time-markdown-viewer)
