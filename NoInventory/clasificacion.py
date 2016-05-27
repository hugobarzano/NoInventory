# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
import unicodedata
from bson.objectid import ObjectId
from pymongo import *
import time
import os
import csv
import json
from item import *
from bson.json_util import dumps
from django.conf import settings

class ClasificacionDriver(object):
    """ ItemsDriver implemeta las funcionalidades CRUD para administrar items """

    def __init__(self):
        # inizializar MongoClient
        # aacceso a la base de datos
        ON_COMPOSE = os.environ.get('COMPOSE')
        ON_HEROKU = os.environ.get('HEROKU')
        self.client = settings.CLIENTE
        #self.client = getattr(settings, "CLIENTE", None)
        if ON_COMPOSE:
            self.database=self.client.get_default_database()
            self.database['tag1']
            self.database['tag2']
            self.database['tag3']
        elif ON_HEROKU:
            self.database=self.client.get_default_database()
            self.database['tag1']
            self.database['tag2']
            self.database['tag3']
        else:
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

    def destroyTotalDriver(self):
        self.database.tag1.remove()
        self.database.tag2.remove()
        self.database.tag3.remove()

####################Generador de identificadores#######################

    def generateLocalizador(self, item,gestorItems,organizacion):
        localizador=""

        if item is not None:
            print item.tag1
            get1 = list(self.database.tag1.find({'VALOR1':item.tag1,'organizacion':organizacion}))
            get2 = list(self.database.tag2.find({'VALOR2':item.tag2,'organizacion':organizacion}))
            get3 = list(self.database.tag3.find({'VALOR3':item.tag3,'organizacion':organizacion}))

            if len(get1) is 0 or len(get2) is 0 or len(get3) is 0:
                raise Exception("imposible generar localizador, faltan tags")
                return localizador
            else:
                cod_correlativo=gestorItems.database.items.find({"tag1":item.tag1,"organizacion":organizacion}).count()
                aux="00000"
                s = aux[ 0 : 5 - len(str(cod_correlativo+1))]
                print "diferencia"
                s=s+str(cod_correlativo+1)
                print s
                #print "Codigo correlativo:"+str(cod_correlativo)
                localizador=get1[0]["CLAVE1"]+get2[0]["CLAVE2"]+get3[0]["CLAVE3"]+s
                print "localizador generado:"
                print localizador
                return localizador
