from django import forms
from NoInventory.models import *

from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
import json

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['items-database']
db2 = client['inventarios-database']


class ItemForm(forms.ModelForm):
    TIPO = (
    ('funcional', 'funcional'),
    ('obsoleto', 'obsoleto'),
    ('perecedero', 'perecedero'),)
    ESTADO=(
    ('presente', 'presente'),
    ('no presente', 'no presente'),
    ('pendiente','pendiente'),)
    nombre_item = forms.CharField(max_length=150, help_text="Introduce el nombre del objeto")
    descripcion_item  = forms.CharField(max_length=300, help_text="Breve descripcion sobre el objeto")
    tag_item = forms.CharField(max_length=150, help_text="Tag para ayudar a clasificar el objeto")
    tipo_item=forms.CharField(max_length=150,widget=forms.Select(choices=TIPO))
    estado_item =forms.CharField(max_length=150,widget=forms.Select(choices=ESTADO))

    class Meta:
        model = Item
        fields = ('nombre_item','descripcion_item','tag_item','tipo_item','estado_item')

class InventarioForm(forms.ModelForm):
    nombre_inventario = forms.CharField(max_length=150, help_text="Introduce el nombre del inventario")
    descripcion_inventario  = forms.CharField(widget = forms.Textarea, help_text="Breve descripcion sobre el inventario")
    tag_inventario = forms.CharField(max_length=150, help_text="Tag para ayudar a clasificar el inventario")
    caracteristicas_inventario = forms.CharField(widget = forms.Textarea, help_text="Caracteristicas del inventario para clasificar los objetos")


    class Meta:
        model = Inventario
        fields = ('nombre_inventario','descripcion_inventario','tag_inventario','caracteristicas_inventario')

class SelectItem(forms.Form):
    tupla= []
    tupla2=[]
    aux2 = []
    aux4 = []
    lista_items=[]
    ESTADO=(
    ('presente', 'presente'),
    ('no presente', 'no presente'),
    ('pendiente','pendiente'),)

    #db2.inventarios.remove()
    #db.items.remove()
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
    items = forms.CharField(max_length=150,widget=forms.Select(choices=SEL2))
    SEL2=[]
