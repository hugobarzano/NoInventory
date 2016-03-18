from bson.objectid import ObjectId
from pymongo import *
import time
import os
from item import *
class Inventario(object):
    """Clase para almacenar informacion de los inventarios"""

    def __init__(self, inventario_id=None,nombre_inventario=None,fecha_alta_inventario=None, descripcion_inventario=None,tag_inventario=None,caracteristicas_inventario=None,items_inventario=[]):

        if inventario_id is None:
            self._id = ObjectId()
        else:
            self._id = inventario_id

        self.nombre_inventario=nombre_inventario
        self.fecha_alta_inventario = time.strftime("%c")
        self.descripcion_inventario = descripcion_inventario
        self.tag_inventario=tag_inventario
        self.caracteristicas_inventario=caracteristicas_inventario
        self.items_inventario=items_inventario


    def get_as_json(self):
        """ Metodo que devuelve el objeto en formato Json, para almacenar en MongoDB """
        return self.__dict__


    @staticmethod
    def build_from_json(json_data):
        """ Metodo usado para contruir objetos inventario apartir de Json"""
        if json_data is not None:
            try:
                #print"Jsonnnn"
                #print json_data
                return Inventario(json_data.get('_id', None),
                    json_data['nombre_inventario'],
                    json_data['fecha_alta_inventario'],
                    json_data['descripcion_inventario'],
                    json_data['tag_inventario'],
                    json_data['caracteristicas_inventario'],
                    json_data['items_inventario'])
            except KeyError as e:
                raise Exception("Clave no encontrada en json: {}".format(e.message))
        else:
            raise Exception("No hay datos para crear un inventario!")


class InventariosDriver(object):
    """ InventariosDriver implemeta las funcionalidades CRUD para administrar inventarios """

    def __init__(self):
        # inizializar MongoClient
        # aacceso a la base de datos
        ON_COMPOSE = os.environ.get('COMPOSE')
        #print ON_COMPOSE
        if ON_COMPOSE:
            self.client = MongoClient('mongodb://172.17.0.2:27017/')
        #    time.sleep(0.01)
        else:
            self.client = MongoClient(host='localhost', port=27017)
        self.database = self.client['inventarios']


    def create(self, inventario):
        if inventario is not None:
            self.database.inventarios.insert(inventario.get_as_json())
        else:
            raise Exception("Imposible crear inventario")


    def read(self, inventario_id=None):
        if inventario_id is None:
            return self.database.inventarios.find()
        else:
            return self.database.inventarios.find({"_id":ObjectId(inventario_id)})


    def update(self, inventario):
        if inventario is not None:
            self.database.inventarios.save(inventario.get_as_json())
        else:
            raise Exception("Imposible actualizar Inventario")


    def delete(self, inventario):
        if inventario is not None:
            self.database.inventarios.remove(inventario.get_as_json())
        else:
            raise Exception("Imposible Borrar Inventario")

    def addToInventario(self,inventario_id,item_id,manejador_item):
        item=manejador_item.read(item_id=item_id)
        if item is not None:
            for i in item:
                item_object = Item.build_from_json(i)
            self.database.inventarios.update({"_id": ObjectId(inventario_id)},{"$addToSet": {"items_inventario" : item_object._id,}})
        else:
            raise Exception("Item no valido para add")

    def destroyDriver(self):
        self.database.inventarios.remove()
