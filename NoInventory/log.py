from bson.objectid import ObjectId
from pymongo import *
import time
from datetime import datetime
import os
from django.conf import settings

class Log(object):
    """Clase para almacenar informacion de los catalogos"""

    def __init__(self, log_id=None,fecha_log=None,organizacion=None,datos_log=None):

        if log_id is None:
            self._id = ObjectId()
        else:
            self._id = log_id
        self.fecha_log = fecha_log
        self.organizacion=organizacion
        self.datos_log=datos_log


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
                return Log(json_data.get('_id', None),
                    json_data['fecha_log'],
                    json_data['organizacion'],
                    json_data['datos_log'])
            except KeyError as e:
                raise Exception("Clave no encontrada en json: {}".format(e.message))
        else:
            raise Exception("No hay datos para crear Log")


class LogDriver(object):
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
            self.database['log']
        elif ON_HEROKU:
            self.database=self.client.get_default_database()
            self.database['log']
        else:
            self.database = self.client['log']


    def create(self, log):
        if log is not None:
            self.database.log.save(log.get_as_json())
        else:
            raise Exception("Imposible crear informe")

    def registrarActividad(self,organizacion,mensaje):
        try:
            print "Organizacion de log"+organizacion
            print "Actividad a registrar"+mensaje
            self.database.log.update({"organizacion": organizacion},{"$addToSet": {"datos_log" :mensaje,}})
        except KeyError as e:
            raise Exception("Imposible Registrar actividad: {}".format(e.message))
