# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
import unicodedata
from bson.objectid import ObjectId
from pymongo import *
import time
import os
from clasificacion import *
from datetime import datetime
from django.conf import settings


def jsonTOstring(elemento):
    #d=json.dumps(elemento)
    texto="id_item:"+str(elemento["_id"])+", nombre_item:" + elemento["nombre_item"] + ",fecha_alta_item :"+elemento["fecha_alta_item"] + ",localizador:"+ elemento["localizador"]
    return texto

class Item(object):
    """Clase para almacenar informacion de los items"""

    def __init__(self, item_id=None,nombre_item=None,fecha_alta_item=None, descripcion_item=None,organizacion=None,usuario=None,tag1=None,tag2=None,tag3=None,peso=None,localizador=None):

        if item_id is None:
            self._id = ObjectId()
        else:
            self._id = item_id
        self.nombre_item=nombre_item
        self.fecha_alta_item = fecha_alta_item
        self.descripcion_item = descripcion_item
        self.organizacion=organizacion
        self.usuario=usuario
        self.tag1=tag1
        self.tag2=tag2
        self.tag3=tag3
        self.peso=peso
        self.localizador=localizador

    def get_as_json(self):
        """ Metodo que devuelve el objeto en formato Json, para almacenar en MongoDB """
        return self.__dict__


    @staticmethod
    def build_from_json(json_data):
        """ Metodo usado para contruir objetos item apartir de Json"""
        if json_data is not None:
            try:
                #print"Jsonnnn"
                #print json_data
                return Item(json_data.get('_id', None),
                    json_data['nombre_item'],
                    json_data['fecha_alta_item'],
                    json_data['descripcion_item'],
                    json_data['organizacion'],
                    json_data['usuario'],
                    json_data['tag1'],
                    json_data['tag2'],
                    json_data['tag3'],
                    json_data['peso'],
                    json_data['localizador'])
            except KeyError as e:
                raise Exception("Clave no encontrada en json: {}".format(e.message))
        else:
            raise Exception("No hay datos para crear un Item!")


class ItemsDriver(object):
    """ ItemsDriver implemeta las funcionalidades CRUD para administrar items """

    def __init__(self):
        # inizializar MongoClient
        # acceso a la base de datos
        ON_COMPOSE = os.environ.get('COMPOSE')
        ON_HEROKU = os.environ.get('HEROKU')
        self.client = settings.CLIENTE
        if ON_COMPOSE:
            self.database=self.client.get_default_database()
            self.database['items']
        elif ON_HEROKU:
            self.database=self.client.get_default_database()
            self.database['items']
        else:
            self.database = self.client['items']



    def create(self, item,clasificador,organizacion):
        if item is not None:
            self.database.items.save(item.get_as_json())
            #self.generateLocalizador(item,clasificador,organizacion)
        else:
            raise Exception("Imposible crear Item")


    def getStringData(self,item):
        if item is not None:
            texto="{\"id_item\":\""+str(item._id)+"\",\"nombre_item\":\"" +item.nombre_item+"\"}"
            return texto
        else:
            raise Exception("Imposible generar los datos en String")



    def read(self, item_id=None):
        if item_id is None:
            return self.database.items.find()
        else:
            return self.database.items.find({"_id":ObjectId(item_id)})


    def update(self, item,clasificador,organizacion):
        if item is not None:
            # the save() method updates the document if this has an _id property
            # which appears in the collection, otherwise it saves the data
            # as a new document in the collection
            self.database.items.save(item.get_as_json())
            #self.generateLocalizador(item,clasificador,organizacion)
        else:
            raise Exception("Imposible actualizar Item")


    def delete(self, item):
        if item is not None:
            self.database.items.remove(item.get_as_json())
        else:
            raise Exception("Imposible Borrar")

    def destroyDriver(self):
        self.database.items.remove()
