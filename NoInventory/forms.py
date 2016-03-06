from django import forms
from django.contrib.auth.models import User
from NoInventory.models import *

from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
import json

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['items-database']
db2 = client['inventarios-database']
db3 = client['entidades-database']



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
    lista_entidades=db3.entidades.find()
    entidad = forms.ChoiceField(label="Entidad", choices=[(x["ENTIDAD"], x["ENTIDAD"]) for x in lista_entidades])


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
    def __init__(self,*args,**kwargs):
        super(SelectItem, self).__init__(*args,**kwargs)
        lista_items=db.items.find()
        self.fields['items'] = forms.ChoiceField(label="items", choices=[(x["nombre_item"], x["nombre_item"]) for x in lista_items])
