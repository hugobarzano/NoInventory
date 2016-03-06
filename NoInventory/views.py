from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import time
from bson import ObjectId
from django.http import HttpResponse
from NoInventory.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['items-database']
db2 = client['inventarios-database']
db3 = client['entidades-database']
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


@csrf_exempt
def inventario2(request,id_inventario):
    nombre_items=[]
    inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
    print "inventario Despues de insertar:"
    print inventario["items_inventario"]
    for i in inventario["items_inventario"]:
        item=db.items.find_one({"_id": i})
        nombre_items.append(item["nombre_item"])
    print nombre_items

    inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
    lista_items=db.items.find()
    form = SelectItem()
    contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
    return render(request, 'noinventory/inventario.html', contexto)




@csrf_exempt
def inventario(request,id_inventario):
    nombre_items=[]
    if request.method == 'POST':
        form = SelectItem(request.POST)
        if form.is_valid():
            print "formulario nombre:"
            print form.data["items"]
            item=db.items.find_one({"nombre_item": form.data["items"]})
            inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
            db2.inventarios.update({"_id": ObjectId(id_inventario)},{"$push": {"items_inventario" :  item["_id"],}})
            inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
            print "inventario Despues de insertar:"
            print inventario["items_inventario"]
            for i in inventario["items_inventario"]:
                item=db.items.find_one({"_id": i})
                nombre_items.append(item["nombre_item"])
            print nombre_items
            lista_items=db.items.find()
            contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
            return render(request, 'noinventory/inventario.html',contexto)
        else:
            print form.errors
    else:
        inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
        form = SelectItem()
        lista_items=db.items.find()
        contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
    return render(request, 'noinventory/inventario.html', contexto)


@csrf_exempt
def addToInventario(request,id_inventario,id_item):
        item=db.items.find_one({"_id": ObjectId(id_item)})
        inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
        db2.inventarios.update({"_id": ObjectId(id_inventario)},{"$addToSet": {"items_inventario" :  item["_id"],}})
        inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
        form = SelectItem()
        lista_items=db.items.find()
        contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
        return render(request, 'noinventory/inventario.html', contexto)

@csrf_exempt
def nuevoItem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            entidad=db3.entidades.find_one({"ENTIDAD":form.data["entidad"]})
            print entidad
            item = {    "nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": time.strftime("%c"),
                        "descripcion_item": form.data['descripcion_item'],
                        "tag_item": form.data['tag_item'],
                        "tipo_item": form.data['tipo_item'],
                        "estado_item": form.data['estado_item'],
                        "codigo_centro":entidad["COD_ENTIDAD"],
                        "centro":entidad["ENTIDAD"],
                        }
            print item
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
@login_required
def nuevoInventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            inventario = {    "nombre_inventario": form.data['nombre_inventario'],
                        "fecha_alta_inventario": time.strftime("%c"),
                        "descripcion_inventario": form.data['descripcion_inventario'],
                        "tag_inventario": form.data['tag_inventario'],
                        "caracteristicas_inventario":form.data['caracteristicas_inventario'],
                        "items_inventario": []
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
