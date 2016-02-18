from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import time
from django.http import HttpResponse
from NoInventory.forms import *

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
            items.insert(item)
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
