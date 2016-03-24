from bson.objectid import ObjectId
from pymongo import *
import time
import os
import csv
import json
from item import *
from bson.json_util import dumps




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


    def createTag1(self, fichero):
        csvfile = open(fichero, 'r')
        fieldnames = ("CLAVE1","VALOR1")
        reader = csv.DictReader( csvfile, fieldnames)
        for row in reader:
            self.database.tag1.insert(row)


    def createTag2(self, fichero):
        csvfile = open(fichero, 'rb')
        fieldnames = ("CLAVE2","VALOR2")
        #reader = csv.reader(open(fichero, 'rb'), delimiter=',')
        reader = csv.DictReader( csvfile, fieldnames)
        for row in reader:
            self.database.tag2.insert(row)

    def createTag3(self, fichero):
        csvfile = open(fichero, 'rb')
        fieldnames = ("CLAVE3","VALOR3")
        #reader = csv.reader(open(fichero, 'rb'), delimiter=',')
        reader = csv.DictReader( csvfile, fieldnames)
        for row in reader:
            print "create 3"
            print row
            self.database.tag3.insert(row)


    def readTag1(self):
        return self.database.tag1.find()

    def readTag2(self):
        return self.database.tag2.find()

    def readTag3(self):
        return self.database.tag3.find()






    def destroyDriver(self):
        self.database.tag1.remove()
        self.database.tag2.remove()
        self.database.tag3.remove()
