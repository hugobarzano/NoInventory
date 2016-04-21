# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
from bson.objectid import ObjectId
#from pymongo.objectid import ObjectId
from pymongo import *
import time
from informe import *
from item import *
from clasificacion import *
import os
from datetime import datetime


def cargar_todos_informes(manejador):
    print("Cargando todos los informes de la base de datos:")
    informes = manejador.read()
    al_menos_uno = False
    for i in informes:
        al_menos_uno = True
        tmp_informe = Informe.build_from_json(i)
        print("ID = {} | Fecha = {}".format(tmp_informe._id,tmp_informe.fecha_informe))
    if not al_menos_uno:
        print("No hay informes en la base de datos")


def test_create(manejador, new_informe):
    print("\n\nGuardando new_informe en la base de datos")
    manejador.create(new_informe)
    print("new_informe guardado en la base de datos")
    print("Cargando new_informe desde la base de datos")
    db_informes = manejador.read(informe_id=new_informe._id)
    for i in db_informes:
        informe = Informe.build_from_json(i)
        print("new_informe = {}".format(informe.get_as_json()))


def test_update(manejador, new_informe):
    print("\n\nActializar new_informe en la base de datos")
    manejador.update(new_informe)
    print("new_informe actualizado en la base de datos")
    print("Recargando new_informe desde la base de datos")
    db_informes = manejador.read(informe_id=new_informe._id)
    for i in db_informes:
        informe = Informe.build_from_json(i)
        print("new_informe = {}".format(informe.get_as_json()))


def test_delete(manejador, new_informe):
    print("\n\nBorrando new_informe de la base de datos")
    manejador.delete(new_informe)
    print("new_informe borrado de la base de datos")
    print("Intentando recargar new_informe de la base de datos")
    db_informes = manejador.read(informe_id=new_informe._id)
    coincidencia = False
    for i in db_informes:
        coincidencia = True
        informe = Informe.build_from_json(i)
        print("new_informe = {}".format(informe.get_as_json()))

    if not coincidencia:
        print("informe con id = {} no ha sido encontrado en la base de datos".format(new_informe._id))


def main():
    manejadorItem = ItemsDriver()
    manejadorClasificacion = ClasificacionDriver()
    manejadorInformes = InformesDriver()



    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#######################################################\n"


    cargar_todos_informes(manejadorInformes)
    new_informe = Informe.build_from_json({"fecha_informe":str(datetime.now()),
        "organizacion":"organizacion",
        "usuario":"usuario",
        "datos_informe":"datos del informe"
    })


    #display all items from DB
    #create new_project and read back from database

    test_create(manejadorInformes, new_informe)


    #update new_item
    #new_catalogo.tipo_catalogo = "Cambiando caracteristicas para actualizar"
    new_informe.usuario="usaurio2"
    test_update(manejadorInformes, new_informe)
    #cargar_todos_catalogos(manejador)

    #delete new_project and try to read back from database
    test_delete(manejadorInformes, new_informe)
    #cargar_todos_catalogos(manejador)

    print "\nLimpiando Base de datos..."
    manejadorInformes.destroyDriver()
    print "Base de datos lista para almacenar informacion\n"



    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
