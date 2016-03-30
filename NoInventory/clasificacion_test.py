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
    manejadorPruebas=ClasificacionPruebas(organizacion="nombre_prueba")

    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA INVENTARIOS"
    print "#######################################################\n"

    #manejadorClasificacion.destroyDriver()
    #manejadorClasificacion.createTag1("Codigo_Centro.csv")
    #manejadorClasificacion.database.tag2.remove()
    manejadorClasificacion.createTag2("Tipo_Dispositivo.csv")
    #manejadorClasificacion.database.tag3.remove()
    #manejadorClasificacion.createTag3("default.csv")
    #salida=manejadorClasificacion.read()
    manejadorPruebas.prueba();
    #aux=manejadorPruebas.database[manejadorPruebas.organizacion].find({'organizacion':'osl'})
    #for i in aux:
    #    print i
    salida=manejadorClasificacion.database.tag2.find({'organizacion':'osl','VALOR2':'CONSUMIBLE'})

    for s in salida:
        print s



    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA INVENTARIOS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
