from django.test import TestCase
from item import *
from catalogo import *
from clasificacion import *
from informe import *

class itemTestCase(TestCase):

    def test_crear_item(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS - CREACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        new_item = Item.build_from_json({"nombre_item":"HP pavilion",
            "fecha_alta_item":time.strftime("%c"),
            "descripcion_item":"Ordenador portatil super potentorro",
            "organizacion":"osl",
            "usuario":"usuario",
            "tag1":"Administracion de  Servicios Centrales",
            "tag2":"MONITOR  CRT",
            "tag3":"DEFAULT",
            "peso":5.2,
            "localizador":"0000000"})
        manejadorItem.create(new_item,manejadorClasificacion,"osl")
        cursor=manejadorItem.database.items.find({"_id":new_item._id})
        for c in cursor:
            item_object=Item.build_from_json(c)
            print("new_item = {}".format(item_object.get_as_json()))

        self.assertEqual(item_object._id,new_item._id)
        self.assertEqual(item_object.nombre_item,new_item.nombre_item)
        self.assertEqual(item_object.fecha_alta_item,new_item.fecha_alta_item)
        self.assertEqual(item_object.descripcion_item,new_item.descripcion_item)
        self.assertEqual(item_object.tag1,new_item.tag1)
        self.assertEqual(item_object.tag2,new_item.tag2)
        self.assertEqual(item_object.tag3,new_item.tag3)
        self.assertEqual(item_object.peso,new_item.peso)
        self.assertEqual(item_object.localizador,new_item.localizador)
        print "\n#######################################################"
        print "ITEM CREADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_borrar_item(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS - ELIMINACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        new_item = Item.build_from_json({"nombre_item":"HP pavilion",
            "fecha_alta_item":time.strftime("%c"),
            "descripcion_item":"Ordenador portatil super potentorro",
            "organizacion":"osl",
            "usuario":"usuario",
            "tag1":"Administracion de  Servicios Centrales",
            "tag2":"MONITOR  CRT",
            "tag3":"DEFAULT",
            "peso":5.2,
            "localizador":"0000000"})
        manejadorItem.create(new_item,manejadorClasificacion,"osl")
        manejadorItem.delete(new_item)
        print("new_item borrado de la base de datos")
        print("Intentando recargar new_item de la base de datos")
        db_items = manejadorItem.read(item_id=new_item._id)
        coincidencia = False
        for i in db_items:
            coincidencia = True
            item_from_db = Item.build_from_json(i)
            print("new_item = {}".format(item_from_db.get_as_json()))

        if not coincidencia:
            self.assertEqual(1,1)
            print("Item con id = {} no ha sido encontrado en la base de datos".format(new_item._id))
        else:
            print "El test de eliminacion no ha sido superado"
            self.assertEqual(1,0)

        print "\n#######################################################"
        print "ITEM ELIMINADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_actualizar_item(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS - ACTUALIZACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        new_item = Item.build_from_json({"nombre_item":"HP pavilion",
            "fecha_alta_item":time.strftime("%c"),
            "descripcion_item":"Ordenador portatil super potentorro",
            "organizacion":"osl",
            "usuario":"usuario",
            "tag1":"Administracion de  Servicios Centrales",
            "tag2":"MONITOR  CRT",
            "tag3":"DEFAULT",
            "peso":5.2,
            "localizador":"0000000"})
        manejadorItem.create(new_item,manejadorClasificacion,"osl")
        new_item.nombre_item="Nombre actualizado"
        manejadorItem.update(new_item,manejadorClasificacion,"osl")

        cursor=manejadorItem.database.items.find({"_id":new_item._id})
        for c in cursor:
            item_object=Item.build_from_json(c)
            print("new_item = {}".format(item_object.get_as_json()))

        self.assertEqual(item_object._id,new_item._id)
        self.assertEqual(item_object.nombre_item,"Nombre actualizado")
        self.assertEqual(item_object.fecha_alta_item,new_item.fecha_alta_item)
        self.assertEqual(item_object.descripcion_item,new_item.descripcion_item)
        self.assertEqual(item_object.tag1,new_item.tag1)
        self.assertEqual(item_object.tag2,new_item.tag2)
        self.assertEqual(item_object.tag3,new_item.tag3)
        self.assertEqual(item_object.peso,new_item.peso)
        self.assertEqual(item_object.localizador,new_item.localizador)
        print "\n#######################################################"
        print "ITEM ACTUALIZADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_destroy_drivers(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - RESTABLECIENDO BASE DE DATOS- "
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        manejadorInformes = InformesDriver()

        manejadorItem.destroyDriver()
        manejadorCatalogo.destroyDriver()
        manejadorClasificacion.destroyTotalDriver()
        manejadorInformes.destroyDriver()
        print "\n#######################################################"
        print "BATERIA DE TEST - BASE DE DATOS RESTABLECIDA - "
        print "#######################################################\n"


class catalogoTestCase(TestCase):

    def test_crear_catalogo(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS - CREACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        new_catalogo = Catalogo.build_from_json({"nombre_catalogo":"Catalogo Elementos A Reciclar",
            "fecha_alta_catalogo":time.strftime("%c"),
            "descripcion_catalogo":"Catalogo con items imposibles de manufacturar. Para reciclaje",
            "organizacion":"organizacion",
            "usuario":"usuario",
            "fecha_alerta_catalogo":time.strftime("%c"),
            "tag_catalogo":"Reciclar",
            "tipo_catalogo":"publico",
            "peso_total":0,
            "id_items_catalogo":[],
            "qr_data":" "})
        manejadorCatalogo.create(new_catalogo)
        cursor=manejadorCatalogo.database.catalogos.find({"_id":new_catalogo._id})
        for c in cursor:
            catalogo_object=Catalogo.build_from_json(c)
            print("new_catalogo = {}".format(catalogo_object.get_as_json()))

        self.assertEqual(catalogo_object.nombre_catalogo,new_catalogo.nombre_catalogo)
        self.assertEqual(catalogo_object.fecha_alta_catalogo,new_catalogo.fecha_alta_catalogo)
        self.assertEqual(catalogo_object.descripcion_catalogo,new_catalogo.descripcion_catalogo)
        self.assertEqual(catalogo_object.organizacion,new_catalogo.organizacion)
        self.assertEqual(catalogo_object.usuario,new_catalogo.usuario)
        self.assertEqual(catalogo_object.fecha_alerta_catalogo,new_catalogo.fecha_alerta_catalogo)
        self.assertEqual(catalogo_object.tag_catalogo,new_catalogo.tag_catalogo)
        self.assertEqual(catalogo_object.tipo_catalogo,new_catalogo.tipo_catalogo)
        self.assertEqual(catalogo_object.peso_total,new_catalogo.peso_total)
        self.assertEqual(catalogo_object.id_items_catalogo,new_catalogo.id_items_catalogo)
        self.assertEqual(catalogo_object.qr_data,str(new_catalogo._id))

        print "\n#######################################################"
        print "CATALOGO CREADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_borrar_catalogo(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS - ELIMINACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        new_catalogo = Catalogo.build_from_json({"nombre_catalogo":"Catalogo Elementos A Reciclar",
            "fecha_alta_catalogo":time.strftime("%c"),
            "descripcion_catalogo":"Catalogo con items imposibles de manufacturar. Para reciclaje",
            "organizacion":"organizacion",
            "usuario":"usuario",
            "fecha_alerta_catalogo":time.strftime("%c"),
            "tag_catalogo":"Reciclar",
            "tipo_catalogo":"publico",
            "peso_total":0,
            "id_items_catalogo":[],
            "qr_data":" "})
        #manejadorCatalogo.create(new_catalogo)
        manejadorCatalogo.delete(new_catalogo)
        print("new_catalogo borrado de la base de datos")
        print("Intentando recargar new_catalogo de la base de datos")
        db_cata = manejadorCatalogo.read(catalogo_id=new_catalogo._id)
        coincidencia = False
        for i in db_cata:
            coincidencia = True
            cata_from_db = Catalogo.build_from_json(i)
            print("new_catalogo = {}".format(cata_from_db.get_as_json()))

        if not coincidencia:
            self.assertEqual(1,1)
            print("Catalogo con id = {} no ha sido encontrado en la base de datos".format(new_catalogo._id))
        else:
            print "El test de eliminacion no ha sido superado"
            self.assertEqual(1,0)

        print "\n#######################################################"
        print "CATALOGO ELIMINADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_actualizar_catalogo(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS - ACTUALIZACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        new_catalogo = Catalogo.build_from_json({"nombre_catalogo":"Catalogo Elementos A Reciclar",
            "fecha_alta_catalogo":time.strftime("%c"),
            "descripcion_catalogo":"Catalogo con items imposibles de manufacturar. Para reciclaje",
            "organizacion":"organizacion",
            "usuario":"usuario",
            "fecha_alerta_catalogo":time.strftime("%c"),
            "tag_catalogo":"Reciclar",
            "tipo_catalogo":"publico",
            "peso_total":0,
            "id_items_catalogo":[],
            "qr_data":" "})
        manejadorCatalogo.create(new_catalogo)
        new_catalogo.nombre_catalogo="Nombre actualizado"
        manejadorCatalogo.update(new_catalogo)

        cursor=manejadorCatalogo.database.catalogos.find({"_id":new_catalogo._id})
        for c in cursor:
            catalogo_object=Catalogo.build_from_json(c)
            print("new_catalogo = {}".format(catalogo_object.get_as_json()))

        self.assertEqual(catalogo_object.nombre_catalogo,"Nombre actualizado")
        self.assertEqual(catalogo_object.fecha_alta_catalogo,new_catalogo.fecha_alta_catalogo)
        self.assertEqual(catalogo_object.descripcion_catalogo,new_catalogo.descripcion_catalogo)
        self.assertEqual(catalogo_object.organizacion,new_catalogo.organizacion)
        self.assertEqual(catalogo_object.usuario,new_catalogo.usuario)
        self.assertEqual(catalogo_object.fecha_alerta_catalogo,new_catalogo.fecha_alerta_catalogo)
        self.assertEqual(catalogo_object.tag_catalogo,new_catalogo.tag_catalogo)
        self.assertEqual(catalogo_object.tipo_catalogo,new_catalogo.tipo_catalogo)
        self.assertEqual(catalogo_object.peso_total,new_catalogo.peso_total)
        self.assertEqual(catalogo_object.id_items_catalogo,new_catalogo.id_items_catalogo)
        self.assertEqual(catalogo_object.qr_data,new_catalogo.qr_data)
        print "\n#######################################################"
        print "CATALOGO ACTUALIZADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_destroy_drivers(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - RESTABLECIENDO BASE DE DATOS- "
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        manejadorInformes = InformesDriver()

        manejadorItem.destroyDriver()
        manejadorCatalogo.destroyDriver()
        manejadorClasificacion.destroyTotalDriver()
        manejadorInformes.destroyDriver()
        print "\n#######################################################"
        print "BATERIA DE TEST - BASE DE DATOS RESTABLECIDA - "
        print "#######################################################\n"


class informeTestCase(TestCase):

    def test_crear_informe(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA INFORMES - CREACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        manejadorInformes = InformesDriver()
        new_informe = Informe.build_from_json({"nombre_informe":"nombre del informe",
            "fecha_informe":"",
            "organizacion":"organizacion",
            "usuario":"usuario",
            "datos_informe":"datos del informe"
        })
        manejadorInformes.create(new_informe)
        cursor=manejadorInformes.database.informes.find({"_id":new_informe._id})
        for c in cursor:
            informe_object=Informe.build_from_json(c)
            print("new_informe = {}".format(informe_object.get_as_json()))

        self.assertEqual(informe_object._id,new_informe._id)
        self.assertEqual(informe_object.nombre_informe,new_informe.nombre_informe)
        self.assertEqual(informe_object.fecha_informe,informe_object.fecha_informe)
        self.assertEqual(informe_object.organizacion,new_informe.organizacion)
        self.assertEqual(informe_object.usuario,new_informe.usuario)
        self.assertEqual(informe_object.datos_informe,new_informe.datos_informe)


        print "\n#######################################################"
        print "INFORME CREADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_borrar_informe(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS - ELIMINACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        manejadorInformes = InformesDriver()

        new_informe = Informe.build_from_json({"nombre_informe":"nombre del informe",
            "fecha_informe":"",
            "organizacion":"organizacion",
            "usuario":"usuario",
            "datos_informe":"datos del informe"
        })
        manejadorInformes.create(new_informe)
        manejadorInformes.delete(new_informe)
        print("new_informe borrado de la base de datos")
        print("Intentando recargar new_informe de la base de datos")
        db_informes = manejadorInformes.read(informe_id=new_informe._id)
        coincidencia = False
        for i in db_informes:
            coincidencia = True
            informe_from_db = Informe.build_from_json(i)
            print("new_informe = {}".format(informe_from_db.get_as_json()))

        if not coincidencia:
            self.assertEqual(1,1)
            print("Informe con id = {} no ha sido encontrado en la base de datos".format(new_informe._id))
        else:
            print "El test de eliminacion no ha sido superado"
            self.assertEqual(1,0)

        print "\n#######################################################"
        print "INFORME ELIMINADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_actualizar_informe(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS - ACTUALIZACION"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        manejadorInformes = InformesDriver()

        new_informe = Informe.build_from_json({"nombre_informe":"nombre del informe",
            "fecha_informe":str(datetime.now()),
            "organizacion":"organizacion",
            "usuario":"usuario",
            "datos_informe":"datos del informe"
        })
        manejadorInformes.create(new_informe)
        new_informe.nombre_informe="Nombre actualizado"
        manejadorInformes.update(new_informe)

        cursor=manejadorInformes.database.informes.find({"_id":new_informe._id})
        for c in cursor:
            informe_object=Informe.build_from_json(c)
            print("new_informe = {}".format(informe_object.get_as_json()))

        self.assertEqual(informe_object._id,new_informe._id)
        self.assertEqual(informe_object.nombre_informe,"Nombre actualizado")
        self.assertEqual(informe_object.fecha_informe,informe_object.fecha_informe)
        self.assertEqual(informe_object.organizacion,new_informe.organizacion)
        self.assertEqual(informe_object.usuario,new_informe.usuario)
        self.assertEqual(informe_object.datos_informe,new_informe.datos_informe)
        print "\n#######################################################"
        print "ITEM ACTUALIZADO CORRECTAMENTE"
        print "#######################################################\n"

    def test_destroy_drivers(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - RESTABLECIENDO BASE DE DATOS- "
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        manejadorInformes = InformesDriver()

        manejadorItem.destroyDriver()
        manejadorCatalogo.destroyDriver()
        manejadorClasificacion.destroyTotalDriver()
        manejadorInformes.destroyDriver()
        print "\n#######################################################"
        print "BATERIA DE TEST - BASE DE DATOS RESTABLECIDA - "
        print "#######################################################\n"



class clasificacionTestCase(TestCase):

    def test_clasificacion(self):
        print "\n#######################################################"
        print "LANZANDO BATERIA DE TEST - CLASIFICACION POR TAGS"
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()

        manejadorClasificacion.createTag1("NoInventory/Codigo_Centro.csv","osl")
        salida=manejadorClasificacion.database.tag1.find({'organizacion':'osl'}).limit(5)
        print "\n#######################################################"
        print "LANZANDO BATERIA DE TEST - CLASIFICACION POR TAG1"
        print "#######################################################\n"
        for s in salida:
            print s
        manejadorClasificacion.createTag2("NoInventory/Tipo_Dispositivo.csv","osl")
        salida=manejadorClasificacion.database.tag2.find({'organizacion':'osl'}).limit(5)
        print "\n#######################################################"
        print "LANZANDO BATERIA DE TEST - CLASIFICACION POR TAG2"
        print "#######################################################\n"
        for s in salida:
            print s
        manejadorClasificacion.createTag3("NoInventory/Estado_Dispositivo.csv","osl")
        salida=manejadorClasificacion.database.tag3.find({'organizacion':'osl'}).limit(5)
        print "\n#######################################################"
        print "LANZANDO BATERIA DE TEST - CLASIFICACION POR TAG3"
        print "#######################################################\n"
        for s in salida:
            print s
        print "\n##########################################################"
        print "FINALIZANDO BATERIA DE TEST - CLASIFICACION POR TAGS"
        print "#########################################################\n"

    def test_destroy_drivers(self):
        print "\n#######################################################"
        print "BATERIA DE TEST - RESTABLECIENDO BASE DE DATOS- "
        print "#######################################################\n"
        manejadorItem = ItemsDriver()
        manejadorCatalogo = CatalogosDriver()
        manejadorClasificacion = ClasificacionDriver()
        manejadorInformes = InformesDriver()

        manejadorItem.destroyDriver()
        manejadorCatalogo.destroyDriver()
        manejadorClasificacion.destroyTotalDriver()
        manejadorInformes.destroyDriver()
        print "\n#######################################################"
        print "BATERIA DE TEST - BASE DE DATOS RESTABLECIDA - "
        print "#######################################################\n"
