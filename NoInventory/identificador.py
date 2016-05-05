from bson.objectid import ObjectId
from pymongo import *
import time
import os
from item import *
from clasificacion import *

class IdentificadorDriver(object):

    def generateQR(self,item):
        qr_data_generated=""
        if item is not None:
            aux=item.get_as_json()
            aux["_id"]=str(aux["_id"])
            data={"_id":str(aux["_id"]),"fecha_alta_item":str(aux["fecha_alta_item"])}
            qr_data_generated=str(data)
            print "qr_data_generated:\n"
            print qr_data_generated
            return qr_data_generated
            #self.database.items.update({"_id":ObjectId(item._id)},{"$set": {"qr_data": qr_data_generated}})
        else:
            raise Exception("Imposible generar QR para el item")
            return qr_data_generated
    #codigo-articulo(00000)+codigo-centro(000000)+tag3(00000)+autoincrementable(00000)
    def generateBarCode(self,item,manejador_clasificacion,organizacion):
        barCode=""
        if item is not None:
            get1 = list(manejador_clasificacion.database.tag1.find({'VALOR1':item.tag1,'organizacion':organizacion}))
            get2 = list(manejador_clasificacion.database.tag2.find({'VALOR2':item.tag2,'organizacion':organizacion}))
            get3 = list(manejador_clasificacion.database.tag3.find({'VALOR3':item.tag3,'organizacion':organizacion}))

            if len(get1) is 0 or len(get2) is 0 or len(get3) is 0:
                raise Exception("imposible generar localizador, faltan tags")
                return barCode
            else:
                barCode=get1[0]["CLAVE1"]+get2[0]["CLAVE2"]+get3[0]["CLAVE3"]
                print "localizador generado:"
                print barCode
                return barCode
        else:
            raise Exception("Imposible generar localizador para el item")
            return barCode
