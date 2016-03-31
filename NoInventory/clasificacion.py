from bson.objectid import ObjectId
from pymongo import *
import time
import os
import csv
import json
from item import *
from bson.json_util import dumps





class ClasificacionPruebas(object):
    """ ItemsDriver implemeta las funcionalidades CRUD para administrar items """

    def __init__(self,organizacion):

        self.organizacion=organizacion
        self.client = MongoClient(host='localhost', port=27017)
        self.database = self.client[organizacion]



    def prueba(self):
        cosa={"prueba":"pruebaaaaa","organizacion":"osl"}
        cosa2={"prueba":"pruebaaaaa","organizacion":"osl2"}
        self.database[self.organizacion].insert(cosa)
        self.database[self.organizacion].insert(cosa2)


    def destroyPrueba(self):
        self.database[self.organizacion].remove({'organizacion':'osl'})




class ClasificacionDriver(object):
    """ ItemsDriver implemeta las funcionalidades CRUD para administrar items """

    def __init__(self):
        # inizializar MongoClient
        # aacceso a la base de datos
        ON_COMPOSE = os.environ.get('COMPOSE')
        #print ON_COMPOSE
        if ON_COMPOSE:
        #    time.sleep(0.1)
            self.client = MongoClient('mongodb://172.17.0.2:27017/')
        #    time.sleep(0.1)
        else:
            self.client = MongoClient(host='localhost', port=27017)
        self.database = self.client['tag1']
        self.database = self.client['tag2']
        self.database = self.client['tag3']


    def createTag1(self, fichero,organizacion):
        self.database.tag1.remove({'organizacion':organizacion})
        csvfile = open(fichero, 'r')
        fieldnames = ("CLAVE1","VALOR1")
        reader = csv.DictReader( csvfile, fieldnames)
        for row in reader:
            row["organizacion"]=organizacion
            self.database.tag1.insert(row)

    def createTag2(self, fichero,organizacion):
        self.database.tag2.remove({'organizacion':organizacion})
        csvfile = open(fichero, 'rb')
        fieldnames = ("CLAVE2","VALOR2")
        #reader = csv.reader(open(fichero, 'rb'), delimiter=',')
        reader = csv.DictReader( csvfile, fieldnames)
        for row in reader:
            row["organizacion"]=organizacion
            self.database.tag2.insert(row)

    def createTag3(self, fichero,organizacion):
        self.database.tag3.remove({'organizacion':organizacion})
        csvfile = open(fichero, 'rb')
        fieldnames = ("CLAVE3","VALOR3")
        #reader = csv.reader(open(fichero, 'rb'), delimiter=',')
        reader = csv.DictReader( csvfile, fieldnames)
        for row in reader:
            row["organizacion"]=organizacion
            self.database.tag3.insert(row)


    def readTag1(self):
        return self.database.tag1.find()

    def readTag2(self):
        return self.database.tag2.find()

    def readTag3(self):
        return self.database.tag3.find()

    def createTag1FromReader(self, reader,organizacion):
        self.database.tag1.remove({'organizacion':organizacion})
        for row in reader:
            row["organizacion"]=organizacion
            self.database.tag1.insert(row)

    def createTag2FromReader(self, reader,organizacion):
        self.database.tag2.remove({'organizacion':organizacion})
        for row in reader:
            row["organizacion"]=organizacion
            self.database.tag2.insert(row)

    def createTag3FromReader(self, reader,organizacion):
        self.database.tag3.remove({'organizacion':organizacion})
        for row in reader:
            row["organizacion"]=organizacion
            self.database.tag3.insert(row)

    def createDefaultTag1(self,organizacion):
        default={"CLAVE1":"00000","VALOR1":"DEFAULT","organizacion":organizacion}
        self.database.tag1.save(default)

    def createDefaultTag2(self,organizacion):
        default={"CLAVE2":"00000","VALOR2":"DEFAULT","organizacion":organizacion}
        self.database.tag2.save(default)

    def createDefaultTag3(self,organizacion):
        default={"CLAVE3":"00000","VALOR3":"DEFAULT","organizacion":organizacion}
        self.database.tag3.save(default)

    def destroyDriver(self,organizacion):
        self.database.tag1.remove({'organizacion':organizacion})
        self.database.tag2.remove({'organizacion':organizacion})
        self.database.tag3.remove({'organizacion':organizacion})
