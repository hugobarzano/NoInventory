from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import time
from django.http import HttpResponse
from NoInventory.forms import *
from django.http import HttpResponseRedirect

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['items-database']
items=db.items

def index(request):
    lista_items=db.items.find()
    contexto = {"lista_items":lista_items}
    return render(request, 'noinventory/index.html',contexto)

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
            id_item=items.insert(item)
            #print id_item
            qr_data_generated=jsonTOstring(items.find_one({"_id": id_item}))
            #print qr_data_generated
            items.update_one({"_id":id_item},{"$set": {"qr_data": qr_data_generated}})
            lista_items=db.items.find()
            #print lista_items
            #for i in lista_items:
                #print i
            contexto = {"lista_items":lista_items}
            return render(request, 'noinventory/index.html',contexto)
        else:
            print form.errors
    else:
        form = ItemForm()
    return render(request, 'noinventory/nuevoItem.html', {'form': form})

def jsonTOstring(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Item:" + elemento["nombre_item"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_item"]+"\nDescripcion:"+elemento["descripcion_item"]+"\nEstado:"+elemento["estado_item"]+"\nTipo:"+elemento["tipo_item"]+"\nTags:"+elemento["tag_item"]
    return texto
