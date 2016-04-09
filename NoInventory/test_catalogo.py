from bson.objectid import ObjectId
#from pymongo.objectid import ObjectId
from pymongo import *
import time
from catalogo import *
from item import *
import os

def cargar_todos_catalogos(manejador):
    print("Cargando todos los catalogos de la base de datos:")
    catalogos = manejador.read()
    al_menos_uno = False
    for i in catalogos:
        al_menos_uno = True
        tmp_invetario = Catalogo.build_from_json(i)
        print("ID = {} |Nombre = {}| Fecha = {}".format(tmp_invetario._id,tmp_invetario.nombre_catalogo,tmp_invetario.fecha_alta_catalogo))
    if not al_menos_uno:
        print("No hay catalogos en la base de datos")


def test_create(manejador, new_catalogo):
    print("\n\nGuardando new_catalogo en la base de datos")
    manejador.create(new_catalogo)
    print("new_catalogo guardado en la base de datos")
    print("Cargando new_catalogo desde la base de datos")
    db_catalogos = manejador.read(catalogo_id=new_catalogo._id)
    for i in db_catalogos:
        catalogos = Catalogo.build_from_json(i)
        print("new_catalogo = {}".format(catalogos.get_as_json()))


def test_update(manejador, new_catalogo):
    print("\n\nActializar new_items en la base de datos")
    manejador.update(new_catalogo)
    print("new_catalogo actualizado en la base de datos")
    print("Recargando new_catalogo desde la base de datos")
    db_catalogos = manejador.read(catalogo_id=new_catalogo._id)
    for i in db_catalogos:
        catalogos = Catalogo.build_from_json(i)
        print("new_catalogo = {}".format(catalogos.get_as_json()))


def test_delete(manejador, new_catalogo):
    print("\n\nBorrando new_catalogo de la base de datos")
    manejador.delete(new_catalogo)
    print("new_catalogo borrado de la base de datos")
    print("Intentando recargar new_catalogo de la base de datos")
    db_catalogos = manejador.read(catalogo_id=new_catalogo._id)
    coincidencia = False
    for i in db_catalogos:
        coincidencia = True
        catalogos = Catalogo.build_from_json(i)
        print("new_catalogo = {}".format(catalogos.get_as_json()))

    if not coincidencia:
        print("Catalogo con id = {} no ha sido encontrado en la base de datos".format(new_catalogo._id))


def main():
    manejador = CatalogosDriver()
    manejadorItem = ItemsDriver()
    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#######################################################\n"


    #cargar_todos_catalogos(manejador)
    new_item = Item.build_from_json({"nombre_item":"HP pavilion",
        "fecha_alta_item":time.strftime("%c"),
        "descripcion_item":"Ordenador portatil super potentorro",
        "tag_item":"Ultrabook, Notebook",
        "tag1":"Administracion de  Servicios Centrales",
        "tag2":"funcional",
        "tag3":"presente",
        "codigo_centro":"06UG02",
        "qr_data":" "})
    manejadorItem.create(new_item)

    #display all items from DB
    #create new_project and read back from database
    new_catalogo = Catalogo.build_from_json({"nombre_catalogo":"Catalogo Elementos A Reciclar",
        "fecha_alta_catalogo":time.strftime("%c"),
        "descripcion_catalogo":"Catalogo con items imposibles de manufacturar. Para reciclaje",
        "tag_catalogo":"Reciclar",
        "caracteristicas_catalogo":"chatarra perjudial para reciclar",
        "items_catalogo":[]})
    test_create(manejador, new_catalogo)

    manejador.addToCatalogo(new_catalogo._id,new_item._id,manejadorItem)

    inven=manejador.read(catalogo_id=new_catalogo._id)
    for i in inven:
        res = Catalogo.build_from_json(i)

    print "items del catalogo"
    print res.items_catalogo
    #cargar_todos_catalogos(manejador)
    #update new_item
    #new_catalogo.caracteristicas_catalogo = "Cambiando caracteristicas para actualizar"
    #test_update(manejador, new_catalogo)
    #cargar_todos_catalogos(manejador)

    #delete new_project and try to read back from database
    #test_delete(manejador, new_catalogo)
    #cargar_todos_catalogos(manejador)

    print "\nLimpiando Base de datos..."
    manejador.destroyDriver()
    print "Base de datos lista para almacenar informacion\n"



    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
