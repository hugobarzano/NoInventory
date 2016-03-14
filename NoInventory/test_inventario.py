from bson.objectid import ObjectId
#from pymongo.objectid import ObjectId
from pymongo import MongoClient
import time
from inventario import *
import os

def cargar_todos_inventarios(manejador):
    print("Cargando todos los inventarios de la base de datos:")
    inventarios = manejador.read()
    al_menos_uno = False
    for i in inventarios:
        al_menos_uno = True
        tmp_invetario = Inventario.build_from_json(i)
        print("ID = {} |Nombre = {}| Fecha = {}".format(tmp_invetario._id,tmp_invetario.nombre_inventario,tmp_invetario.fecha_alta_inventario))
    if not al_menos_uno:
        print("No hay inventarios en la base de datos")


def test_create(manejador, new_inventario):
    print("\n\nGuardando new_inventario en la base de datos")
    manejador.create(new_inventario)
    print("new_inventario guardado en la base de datos")
    print("Cargando new_inventario desde la base de datos")
    db_inventarios = manejador.read(inventario_id=new_inventario._id)
    for i in db_inventarios:
        inventarios = Inventario.build_from_json(i)
        print("new_inventario = {}".format(inventarios.get_as_json()))


def test_update(manejador, new_inventario):
    print("\n\nActializar new_items en la base de datos")
    manejador.update(new_inventario)
    print("new_inventario actualizado en la base de datos")
    print("Recargando new_inventario desde la base de datos")
    db_inventarios = manejador.read(inventario_id=new_inventario._id)
    for i in db_inventarios:
        inventarios = Inventario.build_from_json(i)
        print("new_inventario = {}".format(inventarios.get_as_json()))


def test_delete(manejador, new_inventario):
    print("\n\nBorrando new_inventario de la base de datos")
    manejador.delete(new_inventario)
    print("new_inventario borrado de la base de datos")
    print("Intentando recargar new_inventario de la base de datos")
    db_inventarios = manejador.read(inventario_id=new_inventario._id)
    coincidencia = False
    for i in db_inventarios:
        coincidencia = True
        inventarios = Inventario.build_from_json(i)
        print("new_inventario = {}".format(inventarios.get_as_json()))

    if not coincidencia:
        print("Inventario con id = {} no ha sido encontrado en la base de datos".format(new_inventario._id))


def main():
    manejador = InventariosDriver()
    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA INVENTARIOS"
    print "#######################################################\n"


    cargar_todos_inventarios(manejador)

    #display all items from DB
    #create new_project and read back from database
    new_inventario = Inventario.build_from_json({"nombre_inventario":"Inventario Elementos A Reciclar",
        "fecha_alta_inventario":time.strftime("%c"),
        "descripcion_inventario":"Inventario con items imposibles de manufacturar. Para reciclaje",
        "tag_inventario":"Reciclar",
        "caracteristicas_inventario":"chatarra perjudial para reciclar",
        "items_inventario":"id de prueba"})
    test_create(manejador, new_inventario)
    #cargar_todos_inventarios(manejador)
    #update new_item
    new_inventario.caracteristicas_inventario = "Cambiando caracteristicas para actualizar"
    test_update(manejador, new_inventario)
    #cargar_todos_inventarios(manejador)

    #delete new_project and try to read back from database
    test_delete(manejador, new_inventario)
    cargar_todos_inventarios(manejador)

    print "\nLimpiando Base de datos..."
    manejador.destroyDriver()
    print "Base de datos lista para almacenar informacion\n"



    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA INVENTARIOS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
