from bson.objectid import ObjectId
from pymongo import MongoClient
import time


class Item(object):
    """Clase para almacenar informacion de los items"""

    def __init__(self, item_id=None,nombre_item=None,fecha_alta_item=None, descripcion_item=None,tag_item=None,tipo_item=None,estado_item=None,codigo_centro=None,centro=None):
        if item_id is None:
            self._id = ObjectId()
        else:
            self._id = item_id
        self.nombre_item=nombre_item
        self.fecha_alta_item = time.strftime("%c")
        self.descripcion_item = descripcion_item
        self.tag_item=tag_item
        self.tipo_item=tipo_item
        self.estado_item=estado_item
        self.codigo_centro=codigo_centro
        self.centro=centro

    def get_as_json(self):
        """ Metodo que devuelve el objeto en formato Json, para almacenar en MongoDB """
        return self.__dict__


    @staticmethod
    def build_from_json(json_data):
        """ Metodo usado para contruir objetos item apartir de Json"""
        if json_data is not None:
            try:
                return Item(json_data.get('_id', None),
                    json_data['nombre_item'],
                    json_data['fecha_alta_item'],
                    json_data['descripcion_item'],
                    json_data['tag_item'],
                    json_data['tipo_item'],
                    json_data['estado_item'],
                    json_data['codigo_centro'],
                    json_data['centro'])
            except KeyError as e:
                raise Exception("Clave no encontrada en json: {}".format(e.message))
        else:
            raise Exception("No hay datos para crear un Item!")


class ItemsDriver(object):
    """ ItemsDriver implemeta las funcionalidades CRUD para administrar items """

    def __init__(self):
        # inizializar MongoClient
        # aacceso a la base de datos
        self.client = MongoClient(host='localhost', port=27017)
        self.database = self.client['items']


    def create(self, item):
        if item is not None:
            self.database.items.insert(item.get_as_json())
        else:
            raise Exception("Imposible crear Item")


    def read(self, item_id=None):
        if item_id is None:
            return self.database.items.find({})
        else:
            return self.database.items.find({"_id":item_id})


    def update(self, item):
        if item is not None:
            # the save() method updates the document if this has an _id property
            # which appears in the collection, otherwise it saves the data
            # as a new document in the collection
            self.database.items.save(item.get_as_json())
        else:
            raise Exception("Imposible actualizar Item")


    def delete(self, item):
        if item is not None:
            self.database.items.remove(item.get_as_json())
        else:
            raise Exception("Imposible Borrar")




def load_all_items_from_database(manejador):
    print("Loading all items from database:")
    #items = manejador.read()
    items = []
    at_least_one_item = False
    for i in items:
        at_least_one_item = True
        tmp_item = Item.build_from_json(i)
        #print("ID = {} | Fecha = {}".format(tmp_item._id,tmp_item.fecha_alta_item))
    if not at_least_one_item:
        print("No items in the database")


def test_create(manejador, new_item):
    print("\n\nSaving new_item to database")
    manejador.create(new_item)
    print("new_item saved to database")
    print("Loading new_item from database")
    db_items = manejador.read(item_id=new_item._id)
    for i in db_items:
        items_from_db = Item.build_from_json(i)
        print("new_item = {}".format(items_from_db.get_as_json()))


def test_update(manejador, new_item):
    print("\n\nUpdating new_items in database")
    manejador.update(new_item)
    print("new_item updated in database")
    print("Reloading new_item from database")
    db_items = manejador.read(item_id=new_item._id)
    for i in db_items:
        items_from_db = Item.build_from_json(i)
        print("new_item = {}".format(items_from_db.get_as_json()))


def test_delete(manejador, new_item):
    print("\n\nDeleting new_item to database")
    manejador.delete(new_item)
    print("new_item deleted from database")
    print("Trying to reload new_item from database")
    db_items = manejador.read(item_id=new_item._id)
    coincidencia = False
    for i in db_items:
        coincidencia = True
        items_from_db = Item.build_from_json(i)
        print("new_item = {}".format(item_from_db.get_as_json()))

    if not coincidencia:
        print("Item with id = {} was not found in the database".format(new_item._id))


def main():
    manejador = ItemsDriver()
    (manejador)

    #display all items from DB
    load_all_items_from_database


    #create new_project and read back from database
    new_item = Item.build_from_json({"nombre_item":"HP pavilion",
        "fecha_alta_item":time.strftime("%c"),
        "descripcion_item":"Ordenador portatil super potentorro",
        "tag_item":"Ultrabook, Notebook",
        "tipo_item":"funcional",
        "estado_item":"presente",
        "codigo_centro":"06UG02",
        "centro":"Administracion de  Servicios Centrales"})
    test_create(manejador, new_item)

    #update new_item
    new_item.descripcion_item = "Ordenador portatil nada pontente"
    test_update(manejador, new_item)

    #delete new_project and try to read back from database
    test_delete(manejador, new_item)

if __name__ == '__main__':
    main()
