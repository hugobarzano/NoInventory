from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import time
from bson import ObjectId
from django.http import HttpResponse
from NoInventory.forms import *
from django.http import HttpResponseRedirect

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['items-database']
db2 = client['inventarios-database']
items=db.items
inventarios=db2.inventarios

def index(request):
    lista_items=db.items.find()
    contexto = {"lista_items":lista_items}
    return render(request, 'noinventory/index.html',contexto)

def items(request):
    lista_items=db.items.find()
    contexto = {"lista_items":lista_items}
    return render(request, 'noinventory/items.html',contexto)

def prueba(request):
    form = SelectItem()
    return render(request, 'noinventory/prueba.html', {'form': form})

def inventarios(request):
    lista_inventarios=db2.inventarios.find()
    contexto = {"lista_inventarios":lista_inventarios}
    return render(request, 'noinventory/inventarios.html',contexto)

def inventario(request,id_inventario):
    inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
    lista_inventarios=db2.inventarios.find()
    contexto = {"inventario":inventario}
    return render(request, 'noinventory/inventario.html',contexto)

def agregarObjeto(request,id_inventario,id_objeto):
    inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
    lista_inventarios=db2.inventarios.find()
    contexto = {"inventario":inventario}
    return render(request, 'noinventory/inventario.html',contexto)

@csrf_exempt
def nuevoItem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = {    "nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": time.strftime("%c"),
                        "descripcion_item": form.data['descripcion_item'],
                        "tag_item": form.data['tag_item'],
                        "tipo_item": form.data['tipo_item'],
                        "estado_item": form.data['estado_item'],
                        }
            id_item=db.items.insert(item)
            #print id_item
            qr_data_generated=jsonTOstring(db.items.find_one({"_id": id_item}))
            #print qr_data_generated
            db.items.update_one({"_id":id_item},{"$set": {"qr_data": qr_data_generated}})
            lista_items=db.items.find()
            #print lista_items
            #for i in lista_items:
                #print i
            contexto = {"lista_items":lista_items}
            return render(request, 'noinventory/items.html',contexto)
        else:
            print form.errors
    else:
        form = ItemForm()
    return render(request, 'noinventory/nuevoItem.html', {'form': form})

def jsonTOstring(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Item:" + elemento["nombre_item"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_item"]+"\nDescripcion:"+elemento["descripcion_item"]+"\nEstado:"+elemento["estado_item"]+"\nTipo:"+elemento["tipo_item"]+"\nTags:"+elemento["tag_item"]
    return texto


@csrf_exempt
def nuevoInventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            inventario = {    "nombre_inventario": form.data['nombre_inventario'],
                        "fecha_alta_inventario": time.strftime("%c"),
                        "descripcion_inventario": form.data['descripcion_inventario'],
                        "tag_inventario": form.data['tag_inventario'],
                        "caracteristicas_inventario":form.data['caracteristicas_inventario']
                        }
            id_inventario=db2.inventarios.insert(inventario)
            #print id_item
            qr_data_generated=jsonTOstringInventario(db2.inventarios.find_one({"_id": id_inventario}))
            #print qr_data_generated
            db2.inventarios.update_one({"_id":id_inventario},{"$set": {"qr_data": qr_data_generated}})
            lista_inventarios=db2.inventarios.find()
            #print lista_items
            #for i in lista_items:
                #print i
            contexto = {"lista_inventarios":lista_inventarios}
            return render(request, 'noinventory/inventarios.html',contexto)
        else:
            print form.errors
    else:
        form = InventarioForm()
    return render(request, 'noinventory/nuevoInventario.html', {'form': form})


def jsonTOstringInventario(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Inventario:" + elemento["nombre_inventario"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_inventario"]+"\nDescripcion:"+elemento["descripcion_inventario"]+"\nTags:"+elemento["tag_inventario"]
    return texto
