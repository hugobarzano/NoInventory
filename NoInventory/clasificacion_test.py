from bson.objectid import ObjectId
#from pymongo.objectid import ObjectId
from pymongo import *
import time
from inventario import *
from item import *
from clasificacion import *
import os



def main():
    manejador = InventariosDriver()
    manejadorItem = ItemsDriver()
    manejadorClasificacion=ClasificacionDriver()
    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA INVENTARIOS"
    print "#######################################################\n"


    manejadorClasificacion.createTag1("Codigo_Centro.csv")
    #salida=manejadorClasificacion.read()

    salida=manejadorClasificacion.database.tag1.find()

    for s in salida:
        print s



    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA INVENTARIOS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
