from bson.objectid import ObjectId
from pymongo import *
import time
import os
from item import *
from django.conf import settings

gestorItems=ItemsDriver()
class Catalogo(object):
    """Clase para almacenar informacion de los catalogos"""

    def __init__(self, catalogo_id=None,nombre_catalogo=None,fecha_alta_catalogo=None, descripcion_catalogo=None,organizacion=None,usuario=None,fecha_alerta_catalogo=None,tag_catalogo=None,tipo_catalogo=None,peso_total=None,id_items_catalogo=[],qr_data=None):

        if catalogo_id is None:
            self._id = ObjectId()
        else:
            self._id = catalogo_id

        self.nombre_catalogo=nombre_catalogo
        self.fecha_alta_catalogo = fecha_alta_catalogo
        self.descripcion_catalogo = descripcion_catalogo
        self.organizacion=organizacion
        self.usuario=usuario
        self.fecha_alerta_catalogo=fecha_alerta_catalogo
        self.tag_catalogo=tag_catalogo
        self.tipo_catalogo=tipo_catalogo
        self.peso_total=peso_total
        self.id_items_catalogo=id_items_catalogo
        self.qr_data=qr_data


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
                return Catalogo(json_data.get('_id', None),
                    json_data['nombre_catalogo'],
                    json_data['fecha_alta_catalogo'],
                    json_data['descripcion_catalogo'],
                    json_data['organizacion'],
                    json_data['usuario'],
                    json_data['fecha_alerta_catalogo'],
                    json_data['tag_catalogo'],
                    json_data['tipo_catalogo'],
                    json_data['peso_total'],
                    json_data['id_items_catalogo'],
                    json_data['qr_data'])
            except KeyError as e:
                raise Exception("Clave no encontrada en json: {}".format(e.message))
        else:
            raise Exception("No hay datos para crear un catalogo!")


class CatalogosDriver(object):
    """ CatalogosDriver implemeta las funcionalidades CRUD para administrar catalogos """

    def __init__(self):
        # inizializar MongoClient
        # aacceso a la base de datos
        ON_COMPOSE = os.environ.get('COMPOSE')
        ON_SNAP_CI = os.environ.get('SNAP_CI')
        self.client = getattr(settings, "CLIENTE", None)
        if ON_COMPOSE:
            self.database=self.client.get_default_database()
            self.database['catalogos']
        elif ON_SNAP_CI:
            self.database=self.client.get_default_database()
            self.database['catalogos']
        else:
            self.database = self.client['catalogos']




    def create(self, catalogo):
        if catalogo is not None:
            self.database.catalogos.save(catalogo.get_as_json())
            self.generateQR(catalogo)
        else:
            raise Exception("Imposible crear catalogo")

    def generateQR(self,catalogo):
        if catalogo is not None:
            qr_data_generated=str(catalogo._id)
            self.database.catalogos.update({"_id":catalogo._id},{"$set": {"qr_data": qr_data_generated}})
        else:
            raise Exception("Imposible generar QR para el catalogo")



    def calculatePeso(self,catalogo):
        if catalogo is not None:
            peso=0.0
            print "calculando peso"
            print catalogo.id_items_catalogo
            item_object=Item()
            item_object.peso=0
            for i in catalogo.id_items_catalogo:
                item_aux=gestorItems.database.items.find({"_id":ObjectId(i)})
                for j in item_aux:
                    item_object=Item.build_from_json(j)
                peso=peso+float(item_object.peso)
            self.database.catalogos.update({"_id":catalogo._id},{"$set": {"peso_total": peso}})
        else:
            raise Exception("Imposible calcular peso el catalogo")

    def cleanCatalogo(self,catalogo):
        if catalogo is not None:
            self.database.catalogos.update({"_id":catalogo._id},{"$set": {"id_items_catalogo": []}})
            self.database.catalogos.update({"_id":catalogo._id},{"$set": {"peso_total": 0}})

        else:
            raise Exception("Imposible calcular peso el catalogo")

    def read(self, catalogo_id=None):
        if catalogo_id is None:
            return self.database.catalogos.find()
        else:
            return self.database.catalogos.find({"_id":ObjectId(catalogo_id)})


    def update(self, catalogo):
        if catalogo is not None:
            self.database.catalogos.save(catalogo.get_as_json())
        else:
            raise Exception("Imposible actualizar Catalogo")


    def delete(self, catalogo):
        if catalogo is not None:
            self.database.catalogos.remove(catalogo.get_as_json())
        else:
            raise Exception("Imposible Borrar Catalogo")

    def addToCatalogo(self,catalogo_id,item_id,manejador_item):
        item=manejador_item.read(item_id=item_id)
        if item is not None:
            for i in item:
                item_object = Item.build_from_json(i)
                print item_object.nombre_item
            self.database.catalogos.update({"_id": ObjectId(catalogo_id)},{"$addToSet": {"id_items_catalogo" : str(item_object._id),}})

        else:
            raise Exception("Item no valido para add")

    def removeItemFromCatalogos(self,i_id):
        self.database.catalogos.update({},{"$pull" : {"id_items_catalogo" : str(i_id)}},multi=True)

    def destroyDriver(self):
        self.database.catalogos.remove()
