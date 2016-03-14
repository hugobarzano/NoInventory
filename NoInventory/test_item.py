from bson.objectid import ObjectId
#from pymongo.objectid import ObjectId
from pymongo import MongoClient
import time
from item import *
import os

def load_all_items_from_database(manejador):
    print("Cargando todos los items de la base de datos:")
    items = manejador.read()
    at_least_one_item = False
    for i in items:
        at_least_one_item = True
        tmp_item = Item.build_from_json(i)
        print("ID = {} |Nombre = {}| Fecha = {}".format(tmp_item._id,tmp_item.nombre_item,tmp_item.fecha_alta_item))
    if not at_least_one_item:
        print("No hay items en la base de datos")


def test_create(manejador, new_item):
    print("\n\nGuardando new_item en la base de datos")
    manejador.create(new_item)
    print("new_item guardado en la base de datos")
    print("Cargando new_item desde la base de datos")
    db_items = manejador.read(item_id=new_item._id)
    for i in db_items:
        items_from_db = Item.build_from_json(i)
        print("new_item = {}".format(items_from_db.get_as_json()))


def test_update(manejador, new_item):
    print("\n\nActializar new_items en la base de datos")
    manejador.update(new_item)
    print("new_item actualizado en la base de datos")
    print("Recargando new_item desde la base de datos")
    db_items = manejador.read(item_id=new_item._id)
    for i in db_items:
        items_from_db = Item.build_from_json(i)
        print("new_item = {}".format(items_from_db.get_as_json()))


def test_delete(manejador, new_item):
    print("\n\nBorrando new_item de la base de datos")
    manejador.delete(new_item)
    print("new_item borrado de la base de datos")
    print("Intentando recargar new_item de la base de datos")
    db_items = manejador.read(item_id=new_item._id)
    coincidencia = False
    for i in db_items:
        coincidencia = True
        items_from_db = Item.build_from_json(i)
        print("new_item = {}".format(item_from_db.get_as_json()))

    if not coincidencia:
        print("Item con id = {} no ha sido encontrado en la base de datos".format(new_item._id))


def main():
    manejador = ItemsDriver()
    #manejador.destroyDriver()
    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS"
    print "#######################################################\n"


    load_all_items_from_database(manejador)

    #display all items from DB


    #create new_project and read back from database
    new_item = Item.build_from_json({"nombre_item":"HP pavilion",
        "fecha_alta_item":time.strftime("%c"),
        "descripcion_item":"Ordenador portatil super potentorro",
        "tag_item":"Ultrabook, Notebook",
        "tipo_item":"funcional",
        "estado_item":"presente",
        "codigo_centro":"06UG02",
        "centro":"Administracion de  Servicios Centrales"})
    test_create(manejador, new_item)

    #update new_item
    new_item.descripcion_item = "Ordenador portatil nada pontente"
    test_update(manejador, new_item)
    load_all_items_from_database(manejador)

    #delete new_project and try to read back from database
    test_delete(manejador, new_item)

    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
