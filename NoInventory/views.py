# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
import csv
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import StringIO
import time
from bson import ObjectId
from django.http import HttpResponse
from django.http import HttpResponseServerError
from NoInventory.forms import *
from NoInventory.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from bson.json_util import dumps
import json
import os
from item import *
from catalogo import *
from clasificacion import *
from informe import *
from io import StringIO

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import urllib

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from xhtml2pdf import pisa
from cStringIO import StringIO






gestorItems = ItemsDriver()
gestorCatalogos = CatalogosDriver()
gestorClasificacion=ClasificacionDriver()
gestorInformes = InformesDriver()



from pymongo import MongoClient

ON_COMPOSE = os.environ.get('COMPOSE')
if ON_COMPOSE:
    client = MongoClient('mongodb://172.17.0.2:27017/')
else:
    client = MongoClient('mongodb://localhost:27017/')
db = client['noinventory-database']
#os.environ['DB_PORT_27017_TCP_ADDR']


########################### VISTAS PRINCIPALES #################################


def qrcode(value, alt=None):
    """
    Generate QR Code image from a string with the Google charts API

    http://code.google.com/intl/fr-FR/apis/chart/types.html#qrcodes

    Exemple usage --
    {{ my_string|qrcode:"my alt" }}

    <img src="http://chart.apis.google.com/chart?chs=150x150&amp;cht=qr&amp;chl=my_string&amp;choe=UTF-8" alt="my alt" />
    """

    url = conditional_escape("http://chart.apis.google.com/chart?%s" % \
            urllib.urlencode({'chs':'200x200', 'cht':'qr', 'chl':value, 'choe':'UTF-8'}))
    alt = conditional_escape(alt or value)

    return mark_safe(u"""<img class="qrcode" src="%s" width="200" height="200" alt="%s" />""" % (url, alt))





def index(request):
    #print "variable entorno:"
    #print VAR
    #return redirect('/noinventory/index/')
    return render(request, 'noinventory/index.html')

@csrf_exempt
def items(request):
        lista_tag1=gestorClasificacion.database.tag1.find({"organizacion":request.session['organizacion']})
        lista_tag2=gestorClasificacion.database.tag2.find({"organizacion":request.session['organizacion']})
        lista_tag3=gestorClasificacion.database.tag3.find({"organizacion":request.session['organizacion']})
        lista_items=gestorItems.database.items.find({"organizacion":request.session['organizacion']})
        lista_catalogos=gestorCatalogos.database.catalogos.find({"organizacion":request.session['organizacion']})

        contexto = {'lista_items':lista_items,'lista_catalogos':lista_catalogos,'lista_tag1': lista_tag1,'lista_tag2':lista_tag2,'lista_tag3':lista_tag3}
        return render(request, 'noinventory/items.html',contexto)

@csrf_exempt
def item(request,id_item):
    item_object=Item()

    item=gestorItems.read(item_id=id_item)
    for i in item:
        item_object = Item.build_from_json(i)

    contexto = {"item":item_object,"map":item_object.tag1+', Granada',"id_item":item_object._id}
    return render(request, 'noinventory/item.html',contexto)

def prueba(request):
    lista_items=gestorItems.database.items.find()
    form = SelectItem()
    return render(request, 'noinventory/prueba.html', {'form': form,"lista_items":lista_items, 'indice':5})

@csrf_exempt
def catalogos(request):
    lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.session['username']})
    contexto = {"lista_catalogos":lista_catalogos}
    return render(request, 'noinventory/catalogos.html',contexto)

@csrf_exempt
def catalogo(request,id_catalogo):
    catalogo_object=Catalogo()

    lista_items=gestorItems.database.items.find({"organizacion":request.session['organizacion']})
    catalogo=gestorCatalogos.read(catalogo_id=id_catalogo)
    for i in catalogo:
        catalogo_object = Catalogo.build_from_json(i)

    for j in catalogo_object.items_catalogo:
        print j

    contexto = {"catalogo":catalogo_object,"catalogo_id":id_catalogo,"lista_items":lista_items}
    return render(request, 'noinventory/catalogo.html',contexto)

@csrf_exempt
def catalogoToInforme(request):
    if request.method == 'GET':
        catalogo_object=Catalogo()
        item_object=Item()
        items=[]
        lista_items=gestorItems.database.items.find({"organizacion":request.session['organizacion']})
        catalogo=gestorCatalogos.read(catalogo_id=request.GET["catalogo_id"])
        for i in catalogo:
            catalogo_object = Catalogo.build_from_json(i)
        catalogo_object._id=str(catalogo_object._id)

        for i in catalogo_object.id_items_catalogo:
            item_aux=gestorItems.database.items.find({"organizacion":request.session['organizacion'],"_id":ObjectId(i)})
            for j in item_aux:
                item_object=Item.build_from_json(j)
            item_object._id=str(item_object._id)
            item=item_object.get_as_json()
            items.append(item)

        respuesta={"catalogo":catalogo_object.get_as_json(),"items":items}
        print respuesta
        return JsonResponse(respuesta,safe=False)



@csrf_exempt
def addToCatalogo2(request,id_catalogo,id_item):
        gestorCatalogos.addToCatalogo(id_catalogo,id_item,gestorItems)
        lista_items=gestorItems.read()
        catalogo=gestorCatalogos.read(catalogo_id=id_catalogo)
        catalogo_object=Catalogo()
        for i in catalogo:
            catalogo_object = Catalogo.build_from_json(i)
        contexto = {"catalogo":catalogo_object,"catalogo_id":id_catalogo,"lista_items":lista_items}
        return redirect('/noinventory/catalogo/'+id_catalogo,contexto)

@csrf_exempt
def addSearchToCatalogo(request):
    if request.method == 'GET':
        data_aux=json.loads(request.GET['lista_items'])
        print data_aux
        data=[]
        for i in data_aux:
            if i !=None:
                data.append(i)
        mydic=dict(request.GET)
        print mydic["catalogo_id"][0]
        for i in data:
            print i
            gestorCatalogos.addToCatalogo( str(mydic["catalogo_id"][0]),i,gestorItems)
        return HttpResponse("<strong>Los elementos han sido eliminados</strong>")


@csrf_exempt
def addToCatalogo(request):
    if request.method == 'GET':
        item_id=request.GET["item_id"]
        catalogo_id=request.GET["catalogo_id"]
        aux3=[]
        gestorCatalogos.addToCatalogo(catalogo_id,item_id,gestorItems)
        lista_items=gestorItems.database.items.find({"organizacion":request.session['organizacion']})
        catalogo=gestorCatalogos.read(catalogo_id=catalogo_id)
        catalogo_object=Catalogo()
        for i in catalogo:
            catalogo_object = Catalogo.build_from_json(i)


        for i in catalogo_object.items_catalogo:
            aux3.append(i)
            respuesta={"nombre_items":aux3}

        print "Respuestad del servidor"
        print respuesta
        return JsonResponse(respuesta,safe=False)


#############################busqueda################################################
@csrf_exempt
def busqueda(request):
    aux=[]
    aux2=[]
    aux3=[]
    respuesta={}
    if request.method == 'GET':
        print request.GET["modo_busqueda"]

        if request.GET["modo_busqueda"] == str(0):
            lista_items=gestorItems.database.items.find({"organizacion":request.session['organizacion']})
        if request.GET["modo_busqueda"] == str(1):
            lista_items=gestorItems.database.items.find({"organizacion":request.session['organizacion'], "tag1":request.GET["tag1"]})
        if request.GET["modo_busqueda"] == str(4):
            lista_items=gestorItems.database.items.find({"organizacion":request.session['organizacion'], "fecha_alta_item": { "$regex": request.GET["fecha"] } })
        if request.GET["modo_busqueda"] == str(5):
            lista_items=gestorItems.database.items.find({ "organizacion":request.session['organizacion'],"$or": [ {"nombre_item":{ "$regex": request.GET["texto"] }}, {"descripcion_item":{ "$regex": request.GET["texto"] }} ] })

        contenido=""
        for i in lista_items:
            aux = Item.build_from_json(i)
            aux2 = aux.get_as_json()
            aux2["_id"]=str(aux2["_id"])
            print aux2["nombre_item"]
            contenido = contenido + '<h3>Nombre: ' + aux2["nombre_item"]+' Fecha: '+aux2["fecha_alta_item"]+'</h3>'
            contenido = contenido + '<div id="'+aux2["_id"]+'">'
            contenido = contenido + '<p>'+aux2["descripcion_item"]+'</p>'
            contenido = contenido + '<strong>TAGS</strong><br>'+aux2["tag1"]+'<br>'+aux2["tag2"]+'<br>'+aux2["tag3"]+'<br>'
            contenido = contenido + qrcode(aux2["qr_data"], alt="qr")
            contenido = contenido + '<hr> Localizador: '+aux2["localizador"]+'<hr> Identificador: '+aux2['_id']+'<hr>'
            contenido = contenido + '<hr> Creado por: ' +aux2["usuario"]+ '<hr>Organizacion: '+aux2["organizacion"]+'<hr>'
            contenido = contenido + '<a href="/noinventory/modificarItem/'+aux2["_id"]+'"><button class="btn btn-default btn-xs">Modificar</button> </a>'
            contenido = contenido + '<a href="/noinventory/item/'+aux2["_id"]+'"><button class="btn btn-default btn-xs">Detalles</button> </a>'
            contenido = contenido + '<button class="borrarBoton" data-item="'+aux2["_id"]+'">Borrar</button>'
            contenido = contenido + '</div>'


        contenido = contenido + '</div>'
        return HttpResponse(contenido)

    else:
        print "Entrando por post"
        return HttpResponse("post")


############################ GRAFICOS e informes ################################################
def graficos(request):
    lista_tag1=gestorClasificacion.database.tag1.find({"organizacion":request.session['organizacion']})
    lista_tag2=gestorClasificacion.database.tag2.find({"organizacion":request.session['organizacion']})
    lista_tag3=gestorClasificacion .database.tag3.find({"organizacion":request.session['organizacion']})
    return render(request, 'noinventory/graficos.html', {'lista_tag1': lista_tag1,"lista_tag2":lista_tag2,"lista_tag3":lista_tag3})



def datosTag1_prueba (request):
    if request.method == 'GET':
        dicTag2=dict()
        lista_items=gestorItems.database.items.find({"tag1":request.GET['tag1']})
        for item in lista_items:
            item_object = Item.build_from_json(item)
            #print item_object.nombre_item + " -- "+ item_object.tag1+ " -- "+ item_object.tag2
            dicTag2[item_object.tag2]=0
        #print dicTag2

        lista_items=gestorItems.database.items.find({"tag1":request.GET['tag1']})
        for item in lista_items:
            item_object=Item.build_from_json(item)
            #print "tag2:"+item_object.tag2
            dicTag2[item_object.tag2]=dicTag2[item_object.tag2]+1

        datos={'claveTag2':[],'valorTag2':[]}


        for tag in dicTag2:
            datos['claveTag2'].append(tag)
            datos['valorTag2'].append(dicTag2[tag])

        print datos
    	return JsonResponse(datos, safe=False)
    else:
        return HttpResponse("datosTag1")


def datosTag1 (request):
    if request.method == 'GET':
        dicTag2=dict()
        lista_items=gestorItems.database.items.find({"tag1":request.GET['tag1']})
        for item in lista_items:
            item_object = Item.build_from_json(item)
            #print item_object.nombre_item + " -- "+ item_object.tag1+ " -- "+ item_object.tag2
            dicTag2[item_object.tag2]=0
        #print dicTag2

        lista_items=gestorItems.database.items.find({"tag1":request.GET['tag1']})
        for item in lista_items:
            item_object=Item.build_from_json(item)
            #print "tag2:"+item_object.tag2
            dicTag2[item_object.tag2]=dicTag2[item_object.tag2]+1

        datos1={'clave':[],'valor':[]}


        for tag in dicTag2:
            datos1['clave'].append(tag)
            datos1['valor'].append(dicTag2[tag])
        #############Segundos datos
        dicTag3=dict()
        lista_items=gestorItems.database.items.find({"tag1":request.GET['tag1']})
        for item in lista_items:
            item_object = Item.build_from_json(item)
            #print item_object.nombre_item + " -- "+ item_object.tag1+ " -- "+ item_object.tag2
            dicTag3[item_object.tag3]=0
        #print dicTag2

        lista_items=gestorItems.database.items.find({"tag1":request.GET['tag1']})
        for item in lista_items:
            item_object=Item.build_from_json(item)
            #print "tag2:"+item_object.tag2
            dicTag3[item_object.tag3]=dicTag3[item_object.tag3]+1

        datos2={'clave':[],'valor':[]}


        for tag in dicTag3:
            datos2['clave'].append(tag)
            datos2['valor'].append(dicTag3[tag])

        print datos2

        datos={'datos1':datos1,'datos2':datos2}

        print datos
    	return JsonResponse(datos, safe=False)
    else:
        return HttpResponse("datosTag1")




def datosTag2 (request):
    if request.method == 'GET':
        dicTag1=dict()
        lista_items=gestorItems.database.items.find({"tag2":request.GET['tag2']})
        for item in lista_items:
            item_object = Item.build_from_json(item)
            #print item_object.nombre_item + " -- "+ item_object.tag1+ " -- "+ item_object.tag2
            dicTag1[item_object.tag1]=0
        #print dicTag2

        lista_items=gestorItems.database.items.find({"tag2":request.GET['tag2']})
        for item in lista_items:
            item_object=Item.build_from_json(item)
            #print "tag2:"+item_object.tag2
            dicTag1[item_object.tag1]=dicTag1[item_object.tag1]+1

        datos1={'clave':[],'valor':[]}


        for tag in dicTag1:
            datos1['clave'].append(tag)
            datos1['valor'].append(dicTag1[tag])


        ##################Segundos datos
        dicTag3=dict()
        lista_items=gestorItems.database.items.find({"tag2":request.GET['tag2']})
        for item in lista_items:
            item_object = Item.build_from_json(item)
            #print item_object.nombre_item + " -- "+ item_object.tag1+ " -- "+ item_object.tag2
            dicTag3[item_object.tag3]=0
        #print dicTag2

        lista_items=gestorItems.database.items.find({"tag2":request.GET['tag2']})
        for item in lista_items:
            item_object=Item.build_from_json(item)
            #print "tag2:"+item_object.tag2
            dicTag3[item_object.tag3]=dicTag3[item_object.tag3]+1

        datos2={'clave':[],'valor':[]}


        for tag in dicTag3:
            datos2['clave'].append(tag)
            datos2['valor'].append(dicTag3[tag])

        datos={'datos1':datos1,'datos2':datos2}
        print datos
    	return JsonResponse(datos, safe=False)
    else:
        return HttpResponse("datosTag2")


def datosTag3 (request):
    if request.method == 'GET':
        dicTag1=dict()
        lista_items=gestorItems.database.items.find({"tag3":request.GET['tag3']})
        for item in lista_items:
            item_object = Item.build_from_json(item)
            #print item_object.nombre_item + " -- "+ item_object.tag1+ " -- "+ item_object.tag2
            dicTag1[item_object.tag1]=0
        #print dicTag2

        lista_items=gestorItems.database.items.find({"tag3":request.GET['tag3']})
        for item in lista_items:
            item_object=Item.build_from_json(item)
            #print "tag2:"+item_object.tag2
            dicTag1[item_object.tag1]=dicTag1[item_object.tag1]+1

        datos1={'clave':[],'valor':[]}


        for tag in dicTag1:
            datos1['clave'].append(tag)
            datos1['valor'].append(dicTag1[tag])


        dicTag2=dict()
        lista_items=gestorItems.database.items.find({"tag3":request.GET['tag3']})
        for item in lista_items:
            item_object = Item.build_from_json(item)
            #print item_object.nombre_item + " -- "+ item_object.tag1+ " -- "+ item_object.tag2
            dicTag2[item_object.tag2]=0
        #print dicTag2

        lista_items=gestorItems.database.items.find({"tag3":request.GET['tag3']})
        for item in lista_items:
            item_object=Item.build_from_json(item)
            #print "tag2:"+item_object.tag2
            dicTag2[item_object.tag2]=dicTag2[item_object.tag2]+1

        datos2={'clave':[],'valor':[]}


        for tag in dicTag2:
            datos2['clave'].append(tag)
            datos2['valor'].append(dicTag2[tag])

        datos={'datos1':datos1,'datos2':datos2}
        print datos
    	return JsonResponse(datos, safe=False)
    else:
        return HttpResponse("datosTag3")



def informes(request):
    numeroItems=gestorItems.database.items.find({"usuario":request.session['username']}).count()
    lista_informes=gestorInformes.database.informes.find({"organizacion":request.session['organizacion']})
    lista_catalogos=gestorCatalogos.database.catalogos.find({"organizacion":request.session['organizacion']})
    return render(request, 'noinventory/informes.html', {"lista_catalogos":lista_catalogos,"numeroItems":numeroItems,"lista_informes":lista_informes, 'indice':5})


def generateInformeFromCatalogo(request,catalogo_id):
    numeroItems=gestorItems.database.items.find({"usuario":request.session['username']}).count()
    lista_informes=gestorInformes.database.informes.find({"organizacion":request.session['organizacion']})
    catalogo=gestorCatalogos.read(catalogo_id=catalogo_id)
    catalogo_object=Catalogo()
    for i in catalogo:
        catalogo_object = Catalogo.build_from_json(i)


    datos_catalogo='<h3>Catalogo:'+catalogo_object.nombre_catalogo+"</h3><br>"
    datos_catalogo=datos_catalogo+'<h3>Fecha: '+ catalogo_object.fecha_alta_catalogo+"</h3><br>"
    datos_catalogo=datos_catalogo+'<h3>Lo que sea:</h3><br><p> '+ catalogo_object.descripcion_catalogo+"</p><br>"



    return render(request, 'noinventory/informes.html', {"datos_catalogo":datos_catalogo,"numeroItems":numeroItems,"lista_informes":lista_informes,"catalogo":catalogo_object,"catalogo_id":catalogo_id})




@csrf_exempt
def generaPDF(request):
    objeto_informe=Informe()
    informe=gestorInformes.database.informes.find({"organizacion":request.session['organizacion'],"nombre_informe":request.GET["nombre_informe"]})
    for i in informe:
        objeto_informe = Informe.build_from_json(i)


    pdf = StringIO()
    pisa.CreatePDF(StringIO(objeto_informe.datos_informe.encode('utf-8')), pdf)

    return HttpResponse(pdf.getvalue(),content_type='application/pdf')




@csrf_exempt
def guardarInforme(request):
    if request.method == 'GET':
        informe_flag=False
        informe_aux1=gestorInformes.database.informes.find({"organizacion":request.GET["nombre_informe"]})
        for i in informe_aux1:
            informe_flag=True
            objeto_informe = Informe.build_from_json(i)

        if informe_flag == True:
            objeto_informe.datos_informe=request.GET["datos_informe"]
            gestorInformes.update(objeto_informe)

        else:
            informe = Informe.build_from_json({"nombre_informe":request.GET["nombre_informe"],
                "fecha_informe":str(datetime.now()),
                "organizacion":request.session["organizacion"],
                "usuario":request.session['username'],
                "datos_informe":request.GET["datos_informe"]
            })
            gestorInformes.update(informe)

        informes=[]
        informe_aux=gestorInformes.database.informes.find({"organizacion":request.session['organizacion']})
        for i in informe_aux:
            objeto_informe = Informe.build_from_json(i)
            objeto_informe._id=str(objeto_informe._id)
            informes.append(objeto_informe.get_as_json())

        datos={'informes':informes}
    	return JsonResponse(datos, safe=False)

    else:
        return HttpResponse("informe post")




@csrf_exempt
def visualizarInforme(request):
    if request.method == 'GET':
        objeto_informe={}
        print request.GET["nombre_informe"]
        informe=gestorInformes.database.informes.find({"organizacion":request.session['organizacion'],"nombre_informe":request.GET["nombre_informe"]})
        for i in informe:
            objeto_informe = Informe.build_from_json(i)
        objeto_informe._id=str(objeto_informe._id)

        datos={'informe':objeto_informe.get_as_json()}

        print datos
    	return JsonResponse(datos, safe=False)

    else:
        return HttpResponse("informe post")

############################ ADMINISTRACION DE PREFERENCIAS ##########################

class Preferencias(View):

    def get(self, request):
        print "Entrando por el get"
        form=FormEntrada()
        return render(request, 'noinventory/preferencias.html', {'form': form})

    def post(self, request):
        print "Entrando por el post"
        reader_tag1=None
        reader_tag2=None
        reader_tag3=None
        form = FormEntrada(request.POST, request.FILES)
        if form.is_valid():
        #print "formulario valido"
            ##Frichero 1
            fichero1=request.FILES.get('file_tag1',None)
            if fichero1 is not None:
                fieldnames = ("CLAVE1","VALOR1")
                reader_tag1 = csv.DictReader(request.FILES['file_tag1'], fieldnames)
                if reader_tag1 is None:
                    gestorClasificacion.createDefaultTag1(request.session['organizacion'])
                else:
                    gestorClasificacion.createTag1FromReader(reader_tag1,request.session['organizacion'])
            else:
                gestorClasificacion.createDefaultTag1(request.session['organizacion'])

            ##Fichero 2
            fichero2=request.FILES.get('file_tag2',None)
            if fichero2 is not None:
                fieldnames = ("CLAVE2","VALOR2")
                reader_tag2 = csv.DictReader(request.FILES['file_tag2'], fieldnames)
                if reader_tag2 is None:
                    gestorClasificacion.createDefaultTag2(request.session['organizacion'])
                else:
                    gestorClasificacion.createTag2FromReader(reader_tag2,request.session['organizacion'])
            else:
                gestorClasificacion.createDefaultTag2(request.session['organizacion'])
            #Fichero 3
            fichero3=request.FILES.get('file_tag3',None)
            if fichero3 is not None:
                fieldnames = ("CLAVE3","VALOR3")
                reader_tag3 = csv.DictReader(request.FILES['file_tag3'], fieldnames)
                if reader_tag3 is None:
                    gestorClasificacion.createDefaultTag3(request.session['organizacion'])
                else:
                    gestorClasificacion.createTag3FromReader(reader_tag3,request.session['organizacion'])
            else:
                gestorClasificacion.createDefaultTag3(request.session['organizacion'])
            return redirect('/noinventory/preferencias',{'form':form})
        else:
            print "formulario invalido"
            #form = FormEntrada()
            return render(request, 'noinventory/preferencias.html', {'form': form})


def deleteItems(request):
    gestorItems.destroyDriver()
    return redirect('/noinventory/preferencias')

def deleteInventorys(request):
    gestorCatalogos.destroyDriver()
    return redirect('/noinventory/preferencias')

def deleteInformes(request):
    gestorInformes.destroyDriver()
    return redirect('/noinventory/preferencias')


########################### VISTAS JSON PARA ANDROID ################################
@csrf_exempt
def catalogosJson(request):
    if request.method == 'GET':

        return HttpResponse("catalogos json")
    else:
        default={"_id":"ID","nombre":"Nombre","descripcion":"Descripcion"}
        aux7=[]
        aux7.append(default)
        respuesta={"catalogos":aux7}
        aux=[]
        aux3=[]
        if request.POST["flag"] == "True":
            try:
                lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.POST["username"]})
                for i in lista_catalogos:
                    aux = Catalogo.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_catalogo"],"descripcion":aux2["descripcion_catalogo"]}
                    aux3.append(aux4)
                    respuesta={"catalogos":aux3}
            except KeyError as e:
                raise Exception("No tienes catalogos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)
        else:

            try:
                lista_catalogos=gestorCatalogos.database.catalogos.find({"organizacion":request.POST["organizacion"]})
                for i in lista_items:
                    aux = Catalogo.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_catalogo"],"descripcion":aux2["descripcion_catalogo"]}
                    aux3.append(aux4)
                    respuesta={"catalogos":aux3}
            except KeyError as e:
                raise Exception("Organizacion sin  objetos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)

@csrf_exempt
def itemsJson(request):
    if request.method == 'GET':

        return HttpResponse()
    else:
        default={"_id":"ID","nombre":"Nombre","descripcion":"Descripcion"}
        aux7=[]
        aux7.append(default)
        respuesta={"items":aux7}
        aux=[]
        aux3=[]
        if request.POST["flag"] == "True":

            try:
                lista_items=gestorItems.database.items.find({"usuario":request.POST["username"]})
                for i in lista_items:
                    aux = Item.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_item"],"descripcion":aux2["descripcion_item"]}
                    aux3.append(aux4)
                    respuesta={"items":aux3}
            except KeyError as e:
                raise Exception("No tienes objetos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)
        else:

            try:
                lista_items=gestorItems.database.items.find({"organizacion":request.POST["organizacion"]})
                for i in lista_items:
                    aux = Item.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_item"],"descripcion":aux2["descripcion_item"]}
                    aux3.append(aux4)
                    respuesta={"items":aux3}
            except KeyError as e:
                raise Exception("Organizacion sin  objetos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)


@csrf_exempt
def itemJson(request):
    if request.method == 'GET':
        return HttpResponse("get response")
    else:
        respuesta={""}
        print request.POST["item_id"]
        try:
            lista_items=gestorItems.database.items.find({"_id":ObjectId(request.POST["item_id"])})
            for i in lista_items:
                aux = Item.build_from_json(i)
                aux2=aux.get_as_json()
                aux2["_id"]=str(aux2["_id"])
                respuesta={"_id":aux2["_id"],"nombre":aux2["nombre_item"],"descripcion":aux2["descripcion_item"],"localizador":aux2["localizador"]}
                #aux2=str(respuesta)
                print respuesta
        except KeyError as e:
            raise Exception("No existe objeto : {}".format(e.message))
        return JsonResponse(respuesta,safe=False)

@csrf_exempt
def addItemFromQr(request):
    if request.method == 'POST':
        #print "Dicionario completo"

        mydic=dict(request.POST)

        catalogo=mydic["catalogo"]
        #print "catalogo:"
        #print catalogo[0]
        aux=mydic["scaner"][0]
        #print aux
        buscar = "\'"
        reemplazar_por = "\""
        b=aux.replace(buscar, reemplazar_por)
        #print b
        data_aux=json.loads(b)
        #print data_aux["_id"]
        #print data_aux["fecha_alta_item"]
        #gestorCatalogos.addToCatalogo(mydic["catalogo"],ObjectId(data_aux["_id"]),gestorItems)
        item=gestorItems.read(item_id=data_aux["_id"])
        if item is not None:
            for i in item:
                #print "entra forrrr"
                item_object = Item.build_from_json(i)
        else:
            raise Exception("Item no valido para add")
        #print "Item\n"
        #print item_object.nombre_item

        catalogo=gestorCatalogos.read(catalogo_id=catalogo[0])
        if catalogo is not None:
            for i in catalogo:
                #print "entra forrrr 2"
                catalogo_object = Catalogo.build_from_json(i)
        else:
            raise Exception("Catalogo no valido para add")
        #print "Catalogo\n"
        #print catalogo_object.nombre_catalogo

        #gestorCatalogos.addToCatalogo(catalogo[0],data_aux["_id"],gestorItems)
        gestorCatalogos.database.catalogos.update({"_id": catalogo_object._id},{"$addToSet": {"items_catalogo" : item_object.nombre_item,}})
        return HttpResponse("OK")

    else:
        print "recibido get"
    #    print request.GET['contenido_scaner']
        return HttpResponse("gettttttt")




class AndroidItemCreator(View):
    organizacion=None
    def get(self, request):
        form = ItemForm3(organizacion=request.GET['organizacion'])
        #print request.GET['organizacion']
        #form = ItemForm3(organizacion=request.GET['organizacion'])
        return render(request, 'noinventory/nuevoItem.html', {'form': form})

    def post(self, request):
        form = ItemForm3(request.POST,organizacion=request.GET['organizacion'])
        if form.is_valid():
            item =Item.build_from_json({"nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": time.strftime("%c"),
                        "descripcion_item": form.data['descripcion_item'],
                        "organizacion":request.GET['organizacion'],
                        "usuario":request.GET['organizacion'],
                        "tag1": form.data['tag1'],
                        "tag2": form.data['tag2'],
                        "tag3": form.data['tag3'],
                        "localizador":" ",
                        "qr_data":" ",
                        })
            gestorItems.create(item,gestorClasificacion,request.GET['organizacion'])
            lista_items=gestorItems.read()
            contexto = {"lista_items":lista_items}
            return redirect('/noinventory/items',contexto)
        else:
            return render(request, 'noinventory/nuevoItem.html', {'form': form})






################################## COSAS VARIAS ########################################
def jsonTOstring(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Item:" + elemento["nombre_item"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_item"]+"\nDescripcion:"+elemento["descripcion_item"]+"\nEstado:"+elemento["estado_item"]+"\nTipo:"+elemento["tipo_item"]+"\nTags:"+elemento["organizacion"]
    return texto


def jsonTOstringCatalogo(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Catalogo:" + elemento["nombre_catalogo"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_catalogo"]+"\nDescripcion:"+elemento["descripcion_catalogo"]+"\nTags:"+elemento["tag_catalogo"]
    return texto

def desplegable():
    tupla= []
    tupla2=[]
    aux2 = []
    aux4 = []
    lista_items=[]
    items=db.items.find()
    for i in items:
        lista_items.append(i)

    print "aux6:"
    #print lista_items[0]["nombre_item"]

    for i in lista_items:
        tupla.append(str(i["_id"]))
        tupla.append(str(i["_id"]))

        tupla2.append(i["nombre_item"])
        tupla2.append(i["nombre_item"])

        aux=tuple(tupla)
        aux2.append(aux)
        tupla=[]

        aux3=tuple(tupla2)
        aux4.append(aux3)
        tupla2=[]

    #print tupla
    SEL=tuple(aux2)
    SEL2=tuple(aux4)
    print "tupletizando1"
    print SEL
    print "tupletizando2"
    print SEL2
    return SEL2


######################### GESTION DE ITEMS y CATALOGOS #######################
@csrf_exempt
def borrarItem(request):
    i_id = None
    print "vamos a borrar"
    if request.method == 'GET':
        default={"_id":"ID","nombre":"Nombre","descripcion":"Descripcion"}
        aux7=[]
        aux7.append(default)
        respuesta={"items":aux7}
        aux=[]
        aux3=[]
        i_id = request.GET['id_item']
        print i_id
        gestorItems.database.items.remove( {"_id" : ObjectId(i_id) } )
        print "Borrado completado"
        try:
            #lista_items=gestorItems.database.items.find({"usuario":request.session["username"]})
            lista_items=gestorItems.database.items.find({"usuario":request.session["username"],"organizacion":request.session['organizacion']})
            contenido=""
            for i in lista_items:
                aux = Item.build_from_json(i)
                aux2 = aux.get_as_json()
                aux2["_id"]=str(aux2["_id"])
                print aux2["nombre_item"]
                contenido = contenido + '<h3>Nombre: ' + aux2["nombre_item"]+' Fecha: '+aux2["fecha_alta_item"]+'</h3>'
                contenido = contenido + '<div id="'+aux2["_id"]+'">'
                contenido = contenido + '<p>'+aux2["descripcion_item"]+'</p>'
                contenido = contenido + '<strong>TAGS</strong><br>'+aux2["tag1"]+'<br>'+aux2["tag2"]+'<br>'+aux2["tag3"]+'<br>'
                contenido = contenido + qrcode(aux2["qr_data"], alt="qr")
                contenido = contenido + '<hr> Localizador: '+aux2["localizador"]+'<hr> Identificador: '+aux2['_id']+'<hr>'
                contenido = contenido + '<hr> Creado por: ' +aux2["usuario"]+ '<hr>Organizacion: '+aux2["organizacion"]+'<hr>'
                contenido = contenido + '<a href="/noinventory/modificarItem/'+aux2["_id"]+'"><button class="btn btn-default btn-xs">Modificar</button> </a>'
                contenido = contenido + '<a href="/noinventory/item/'+aux2["_id"]+'"><button class="btn btn-default btn-xs">Detalles</button> </a>'
                contenido = contenido + '<button class="borrarBoton" data-item="'+aux2["_id"]+'">Borrar</button>'
                contenido = contenido + '</div>'
            contenido = contenido + '</div>'
        except KeyError as e:
            raise Exception("No tienes objetos asociados : {}".format(e.message))
        return HttpResponse(contenido)

@csrf_exempt
def borrarItems(request):
    if request.method == 'GET':
        data_aux=json.loads(request.GET['lista_items'])
        for i in data_aux:
            gestorItems.database.items.remove( {"_id" : ObjectId(i) } )
        return HttpResponse("<strong>Los elementos han sido eliminados</strong>")




class ItemCreator(View):

    def get(self, request):
        form = ItemForm3(organizacion=request.session['organizacion'])
        #print request.GET['organizacion']
        #form = ItemForm3(organizacion=request.GET['organizacion'])
        return render(request, 'noinventory/nuevoItem.html', {'form': form})

    def post(self, request):
        form = ItemForm3(request.POST,organizacion=request.session['organizacion'])
        if form.is_valid():
            item =Item.build_from_json({"nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": time.strftime("%c"),
                        "descripcion_item": form.data['descripcion_item'],
                        "organizacion": request.session["organizacion"],
                        "usuario":request.session['username'],
                        "tag1": form.data['tag1'],
                        "tag2": form.data['tag2'],
                        "tag3": form.data['tag3'],
                        "localizador":" ",
                        "qr_data":" ",
                        })
            gestorItems.create(item,gestorClasificacion,request.session['organizacion'])
            lista_items=gestorItems.database.items.find({"usuario":request.session["username"]})
            contexto = {"lista_items":lista_items}
            return redirect('/noinventory/items',contexto)
        else:
            return render(request, 'noinventory/nuevoItem.html', {'form': form})


class ItemUpdater(View):

    def get(self, request,id_item):
        cursor=gestorItems.read(item_id=id_item)
        for i in cursor:
            currentItem = Item.build_from_json(i)

        aux=currentItem.get_as_json()
        print aux
        form = ItemForm3(aux,organizacion=request.session['organizacion'])
        form.data["descripcion_item"]=str(form.data["descripcion_item"])+"\nUltima modificacion: "+time.strftime("%c")
        #form.data["tag1"]=aux["tag1"]
        return render(request, 'noinventory/modificarItem.html', {'form': form,'id_item':currentItem._id})

    def post(self, request,id_item):
        cursor=gestorItems.read(item_id=id_item)
        for i in cursor:
            c = Item.build_from_json(i)
        form = ItemForm3(request.POST,organizacion=request.session['organizacion'])
        if form.is_valid():
            itemUpdated =Item.build_from_json({"_id":c._id,
                        "nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": c.fecha_alta_item,
                        "descripcion_item": form.data['descripcion_item'],
                        "organizacion": c.organizacion,
                        "usuario":c.usuario,
                        "tag1":form.data["tag1"],
                        "tag2": form.data['tag2'],
                        "tag3": form.data['tag3'],
                        "localizador":c.localizador,
                        "qr_data":c.qr_data,
                        })
            gestorItems.update(itemUpdated,gestorClasificacion,request.session['organizacion'])
            lista_items=gestorItems.database.items.find({"usuario":request.session["username"]})
            contexto = {"lista_items":lista_items}
            return redirect('/noinventory/items',contexto)
        else:
            print form.errors
            return render(request, 'noinventory/modificarItem.html', {'form': form,'id_item':id_item})

class CatalogoCreator(View):

    def get(self, request):
        form = CatalogoForm()
        return render(request, 'noinventory/nuevoCatalogo.html', {'form': form})

    def post(self, request):
        form = CatalogoForm(request.POST)
        if form.is_valid():
            catalogo =Catalogo.build_from_json({"nombre_catalogo": form.data['nombre_catalogo'],
                        "fecha_alta_catalogo": time.strftime("%c"),
                        "descripcion_catalogo": form.data['descripcion_catalogo'],
                        "organizacion": request.session["organizacion"],
                        "usuario":request.session['username'],
                        "tag_catalogo": form.data['tag_catalogo'],
                        "tipo_catalogo":form.data['tipo_catalogo'],
                        "items_catalogo": [],
                        "id_items_catalogo": [],
                        "qr_data":" ",
                        })
            gestorCatalogos.create(catalogo)
            lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.session["username"]})
            contexto = {"lista_catalogos":lista_catalogos}
            return redirect('/noinventory/catalogos',contexto)
        else:
            print form.errors
            return render(request, 'noinventory/nuevoCatalogo.html', {'form': form})


class CatalogoUpdater(View):

    def get(self, request,id_catalogo):
        cursor=gestorCatalogos.read(catalogo_id=id_catalogo)
        currentcatalogo=Catalogo()
        for i in cursor:
            currentcatalogo = Catalogo.build_from_json(i)
        aux=currentcatalogo.get_as_json()
        form = CatalogoForm(aux)
        form.data["descripcion_catalogo"]=str(form.data["descripcion_catalogo"])+"\nUltima modificacion: "+time.strftime("%c")
        return render(request, 'noinventory/modificarCatalogo.html', {'form': form,'id_catalogo':currentcatalogo._id})

    def post(self, request,id_catalogo):
        cursor=gestorCatalogos.read(catalogo_id=id_catalogo)
        for i in cursor:
            c = Catalogo.build_from_json(i)
        form = CatalogoForm(request.POST)
        if form.is_valid():
            catalogoUpdated =Catalogo.build_from_json({"_id":c._id,
                        "nombre_catalogo": form.data['nombre_catalogo'],
                        "fecha_alta_catalogo": c.fecha_alta_catalogo,
                        "descripcion_catalogo": form.data['descripcion_catalogo'],
                        "organizacion": c.organizacion,
                        "usuario":c.usuario,
                        "tag_catalogo": form.data['tag_catalogo'],
                        "tipo_catalogo": form.data['tipo_catalogo'],
                        "items_catalogo": c.items_catalogo,
                        "id_items_catalogo": c.id_items_catalogo,
                        "qr_data":c.qr_data,
                        })
            gestorCatalogos.update(catalogoUpdated)
            lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.session["username"]})
            contexto = {"lista_catalogos":lista_catalogos}
            return redirect('/noinventory/catalogo/'+str(c._id),contexto)
        else:
            return render(request, 'noinventory/modificarCatalogo.html', {'form': form,'id_catalogo':id_catalogo})




######################### REGISTRO DE USUARIOS ############################################

@csrf_exempt
def androidLogin(request):
    if request.method=='POST':

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                u=User.objects.get(username=user.username)
                user_profile = UserProfile.objects.get(user=user)
                login(request, user)
                #data="nombre_usuario :"+username
                return HttpResponse(user_profile.__organizacion__())
            else:
                return HttpResponse("Your No-Inventory account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        print "entrando por get"
    return HttpResponse()


@csrf_exempt
def androidRegister(request):
    if request.method=='POST':
        #print request.POST["username"]
        #print request.POST["email"]
         #print request.POST["password"]
        #print request.POST["organizacion"]

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid():
            if profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return HttpResponse("success")
            else:
                return HttpResponse("Invalid User or Organizacion")
        else:
            return HttpResponse("Username exist or Invalid Email")
    else:
        print "entrando por get"
    return HttpResponse()


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            return HttpResponseRedirect('/noinventory/')
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            return redirect('registration/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

            #print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'registration/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                u=User.objects.get(username=user.username)
                request.session['username'] = u.username
                user_profile = UserProfile.objects.get(user=user)
                #print user_profile.__organizacion__()
                request.session['organizacion'] = user_profile.__organizacion__()
                login(request, user)
                return HttpResponseRedirect('/noinventory/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your No-Inventory account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'registration/login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    del request.session['username']
    del request.session['organizacion']
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/noinventory/')
