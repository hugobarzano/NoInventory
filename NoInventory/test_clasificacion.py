from bson.objectid import ObjectId

#from pymongo.objectid import ObjectId
from pymongo import *
import time
from catalogo import *
from item import *
from clasificacion import *
import os



def main():
    manejador = CatalogosDriver()
    manejadorItem = ItemsDriver()
    manejadorClasificacion=ClasificacionDriver()
    manejadorPruebas=ClasificacionPruebas(organizacion="nombre_prueba")

    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#######################################################\n"

    manejadorClasificacion.destroyDriver("osl")
    manejadorClasificacion.createTag1("Codigo_Centro.csv","osl")
    #manejadorClasificacion.database.tag2.remove()
    manejadorClasificacion.createTag2("Tipo_Dispositivo.csv","osl")
    #manejadorClasificacion.database.tag3.remove()
    manejadorClasificacion.createTag3("default.csv","osl")
    #salida=manejadorClasificacion.read()
    #manejadorPruebas.prueba();
    #manejadorPruebas.destroyPrueba()
    #aux=manejadorPruebas.database[manejadorPruebas.organizacion].find()

    #for i in aux:
    #    print i
    salida=manejadorClasificacion.database.tag1.find()
    #salida=manejadorClasificacion.database.tag2.find({'organizacion':'osl','VALOR2':'CONSUMIBLE'})

    for s in salida:
        print s



    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
