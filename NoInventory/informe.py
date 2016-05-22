from bson.objectid import ObjectId
from pymongo import *
import time
from datetime import datetime
import os
from item import *
from django.conf import settings

class Informe(object):
    """Clase para almacenar informacion de los catalogos"""

    def __init__(self, informe_id=None,nombre_informe=None,fecha_informe=None,organizacion=None,usuario=None,datos_informe=None):

        if informe_id is None:
            self._id = ObjectId()
        else:
            self._id = informe_id
        self.nombre_informe = nombre_informe
        self.fecha_informe = str(datetime.now())
        self.organizacion=organizacion
        self.usuario=usuario
        self.datos_informe=datos_informe


    def get_as_json(self):
        """ Metodo que devuelve el objeto en formato Json, para almacenar en MongoDB """
        return self.__dict__


    @staticmethod
    def build_from_json(json_data):
        """ Metodo usado para contruir objetos catalogo apartir de Json"""
        if json_data is not None:
            try:
                #print"Jsonnnn"
                #print json_data
                return Informe(json_data.get('_id', None),
                    json_data['nombre_informe'],
                    json_data['fecha_informe'],
                    json_data['organizacion'],
                    json_data['usuario'],
                    json_data['datos_informe'])
            except KeyError as e:
                raise Exception("Clave no encontrada en json: {}".format(e.message))
        else:
            raise Exception("No hay datos para crear un catalogo!")


class InformesDriver(object):
    """ CatalogosDriver implemeta las funcionalidades CRUD para administrar catalogos """

    def __init__(self):
        # inizializar MongoClient
        # aacceso a la base de datos
        ON_COMPOSE = os.environ.get('COMPOSE')
        ON_HEROKU = os.environ.get('HEROKU')
        self.client = settings.CLIENTE
        #self.client = getattr(settings, "CLIENTE", None)
        if ON_COMPOSE:
            self.database=self.client.get_default_database()
            self.database['informes']
        elif ON_HEROKU:
            self.database=self.client.get_default_database()
            self.database['informes']
        else:
            self.database = self.client['informes']


    def create(self, informe):
        if informe is not None:
            self.database.informes.save(informe.get_as_json())
        else:
            raise Exception("Imposible crear informe")




    def read(self, informe_id=None):
        if informe_id is None:
            return self.database.informes.find()
        else:
            return self.database.informes.find({"_id":ObjectId(informe_id)})


    def update(self, informe):
        if informe is not None:
            self.database.informes.save(informe.get_as_json())
        else:
            raise Exception("Imposible actualizar Informe")


    def delete(self, informe):
        if informe is not None:
            self.database.informes.remove(informe.get_as_json())
        else:
            raise Exception("Imposible Borrar informe")


    def destroyDriver(self):
        self.database.informes.remove()
