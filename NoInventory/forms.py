from django import forms
from django.contrib.auth.models import User
from NoInventory.models import *

from clasificacion import *

from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
import json
import os
from NoInventory.views import *


from django.template import RequestContext
from django.forms import ClearableFileInput
from pymongo import MongoClient

ON_COMPOSE = os.environ.get('COMPOSE')
if ON_COMPOSE:
    client = MongoClient('mongodb://172.17.0.2:27017/')
else:
    client = MongoClient('mongodb://localhost:27017/')
db = client['noinventory-database']



manejadorClasificacion=ClasificacionDriver()


class ItemForm3(forms.Form):
    """Form for adding and editing backups."""

    def __init__(self, *args, **kwargs):
        organizacion = kwargs.pop('organizacion')
        super(ItemForm3, self).__init__(*args, **kwargs)
        self.fields['nombre_item'] = forms.CharField(required=True,max_length=150, help_text="Introduce el nombre del objeto")
        self.fields['descripcion_item']  = forms.CharField(widget = forms.Textarea, help_text="Breve descripcion sobre el objeto")
        lista_tag1=manejadorClasificacion.database.tag1.find({"organizacion":organizacion})
        lista_tag2=manejadorClasificacion.database.tag2.find({"organizacion":organizacion})
        lista_tag3=manejadorClasificacion.database.tag3.find({"organizacion":organizacion})
        #print "formulario"
        #print lista_tag2[0]["VALOR2"]
        self.fields['tag1'] = forms.ChoiceField(label="TAG 1", choices=[(x["VALOR1"], x["VALOR1"]) for x in lista_tag1])
        self.fields['tag2'] = forms.ChoiceField(label=lista_tag2[0]["VALOR2"], choices=[(x["VALOR2"], x["VALOR2"]) for x in lista_tag2])
        self.fields['tag3'] = forms.ChoiceField(label="TAG 3", choices=[(x["VALOR3"], x["VALOR3"]) for x in lista_tag3])
        self.fields['peso'] = forms.FloatField(required=False, label='Peso/Unidad',initial=0.0)
        self.fields['unidades']=forms.IntegerField(required=True,label='Unidades',initial=1)



def ItemForm(organizacion):
    print organizacion

    class form_base(forms.Form):

        lista_tag1=manejadorClasificacion.database.tag1.find({"organizacion":organizacion})
        lista_tag2=manejadorClasificacion.database.tag2.find({"organizacion":organizacion})
        lista_tag3=manejadorClasificacion.database.tag3.find({"organizacion":organizacion})

        nombre_item = forms.CharField(required=True,max_length=150, help_text="Introduce el nombre del objeto")
        descripcion_item  = forms.CharField(widget = forms.Textarea, help_text="Breve descripcion sobre el objeto")
        tag_item = forms.CharField(required=True, max_length=150, help_text="Tag para ayudar a clasificar el objeto")
        tag1 = forms.ChoiceField(label="TAG 1", choices=[(x["VALOR1"], x["VALOR1"]) for x in lista_tag1])
        tag2 = forms.ChoiceField(label="TAG 2", choices=[(x["VALOR2"], x["VALOR2"]) for x in lista_tag2])
        tag3 = forms.ChoiceField(label="TAG 3", choices=[(x["VALOR3"], x["VALOR3"]) for x in lista_tag3])

    return form_base



class CatalogoForm(forms.ModelForm):
    TIPO = (('Publico', 'Publico'),('Privado', 'Privado'),)
    nombre_catalogo = forms.CharField(max_length=150, help_text="Introduce el nombre del catalogo")
    descripcion_catalogo  = forms.CharField(widget = forms.Textarea, help_text="Breve descripcion sobre el catalogo")
    tag_catalogo = forms.CharField(max_length=150, help_text="Tag para ayudar a clasificar el catalogo")
    tipo_catalogo = forms.CharField(max_length=150,widget=forms.Select(choices=TIPO))

    class Meta:
        model = Catalogo
        fields = ('nombre_catalogo','descripcion_catalogo','tag_catalogo','tipo_catalogo')

class SelectItem(forms.Form):
    def __init__(self,*args,**kwargs):
        super(SelectItem, self).__init__(*args,**kwargs)
        lista_items=db.items.find()
        self.fields['items'] = forms.ChoiceField(label="items", choices=[(x["nombre_item"], x["nombre_item"]) for x in lista_items])

class DocumentForm(forms.Form):
    archivo = forms.FileField(label='Selecciona fichero csv',help_text='max. 42 megabytes')

class CustomClearableFileInput(ClearableFileInput):
    template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

class FormEntrada(forms.Form):
    file_tag1 = forms.FileField(label='Selecciona un archivo para tag 1',required=False)
    file_tag2 = forms.FileField(label='Selecciona un archivo para tag 2',required=False)
    file_tag3 = forms.FileField(label='Selecciona un archivo para tag 3',required=False)

    #file_tag2 = forms.FileField(label='Selecciona un archivo para tag 2')
    #file_tag3 = forms.FileField(label='Selecciona un archivo para tag 3')




############### REGISTRO DE USUARIOS #################
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('organizacion',)
