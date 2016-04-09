from bson.objectid import ObjectId
from pymongo import *
import time
import os
from clasificacion import *



def jsonTOstring(elemento):
    #d=json.dumps(elemento)
    texto="id_item:"+str(elemento["_id"])+", nombre_item:" + elemento["nombre_item"] + ",fecha_alta_item :"+elemento["fecha_alta_item"] + ",localizador:"+ elemento["localizador"]
    return texto

class Item(object):
    """Clase para almacenar informacion de los items"""

    def __init__(self, item_id=None,nombre_item=None,fecha_alta_item=None, descripcion_item=None,organizacion=None,usuario=None,tag1=None,tag2=None,tag3=None,localizador=None,qr_data=None):

        if item_id is None:
            self._id = ObjectId()
        else:
            self._id = item_id
        self.nombre_item=nombre_item
        self.fecha_alta_item = time.strftime("%c")
        self.descripcion_item = descripcion_item
        self.organizacion=organizacion
        self.usuario=usuario
        self.tag1=tag1
        self.tag2=tag2
        self.tag3=tag3
        self.localizador=localizador
        self.qr_data=qr_data

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
                    json_data['localizador'],
                    json_data['qr_data'])
            except KeyError as e:
                raise Exception("Clave no encontrada en json: {}".format(e.message))
        else:
            raise Exception("No hay datos para crear un Item!")


class ItemsDriver(object):
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
            time.sleep(0.1)
            self.client = MongoClient(host='localhost', port=27017)
        #    time.sleep(0.1)
        self.database = self.client['items']


    def create(self, item,clasificador,organizacion):
        if item is not None:
            self.database.items.insert(item.get_as_json())
            self.generateLocalizador(item,clasificador,organizacion)
            self.generateQR(item)
        else:
            raise Exception("Imposible crear Item")

    def generateQR(self,item):
        if item is not None:
            #qr_data_generated=jsonTOstring(item.get_as_json())
            #qr_data_generated=self.getStringData(item)
            qr_data_generated=str(item.get_as_json())
            print "qr_data_generated:\n"
            print qr_data_generated
            self.database.items.update({"_id":item._id},{"$set": {"qr_data": qr_data_generated}})
        else:
            raise Exception("Imposible generar QR para el item")

    def getStringData(self,item):
        if item is not None:
            texto="{\"id_item\":\""+str(item._id)+"\",\"nombre_item\":\"" +item.nombre_item+"\"}"
            return texto
        else:
            raise Exception("Imposible generar los datos en String")

    def generateLocalizador(self,item,manejador_clasificacion,organizacion):
        if item is not None:
            get1 = list(manejador_clasificacion.database.tag1.find({'VALOR1':item.tag1,'organizacion':organizacion}))
            get2 = list(manejador_clasificacion.database.tag2.find({'VALOR2':item.tag2,'organizacion':organizacion}))
            get3 = list(manejador_clasificacion.database.tag3.find({'VALOR3':item.tag3,'organizacion':organizacion}))

            if len(get1) is 0 or len(get2) is 0 or len(get3) is 0:
                raise Exception("imposible generar localizador")
            else:
                localizador=get1[0]["CLAVE1"]+get2[0]["CLAVE2"]+get3[0]["CLAVE3"]
                print "localizador generado:"
                print localizador
                self.database.items.update({"_id":item._id},{"$set": {"localizador": localizador}})

        else:
            raise Exception("Imposible generar localizador para el item")


    def read(self, item_id=None):
        if item_id is None:
            return self.database.items.find()
        else:
            return self.database.items.find({"_id":ObjectId(item_id)})


    def update(self, item,clasificador):
        if item is not None:
            # the save() method updates the document if this has an _id property
            # which appears in the collection, otherwise it saves the data
            # as a new document in the collection
            self.database.items.save(item.get_as_json())
            self.generateLocalizador(item,clasificador)
            self.generateQR(item)
        else:
            raise Exception("Imposible actualizar Item")


    def delete(self, item):
        if item is not None:
            self.database.items.remove(item.get_as_json())
        else:
            raise Exception("Imposible Borrar")

    def destroyDriver(self):
        self.database.items.remove()
