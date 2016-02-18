from django import forms
from NoInventory.models import *

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
