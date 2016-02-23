from django import forms
from NoInventory.models import *

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['items-database']


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
    aux2 = []
    ESTADO=(
    ('presente', 'presente'),
    ('no presente', 'no presente'),
    ('pendiente','pendiente'),)
    items=db.items.find()
    print items[1]
    #for i in items:
    for i in range(2):
        #print i["_id"]
        #tupla.append(str(items[i]["_id"])+","+str(items[i]["_id"]))
        tupla.append(str(items[i]["_id"]))
        tupla.append(str(items[i]["_id"]))
        aux=tuple(tupla)
        aux2.append(aux)

    print tupla
    SEL=tuple(aux2)
    print "tupletizando"
    print SEL
    print "ESTADO"
    print ESTADO
    #print tupla
    items = forms.CharField(max_length=150,widget=forms.Select(choices=ESTADO))

    #items = forms.ModelChoiceField(db.items.find())
