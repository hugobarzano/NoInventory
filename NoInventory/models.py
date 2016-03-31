from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,primary_key=True)

    # The additional attributes we wish to include.
    organizacion = models.CharField(max_length=150,blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.organizacion

    def __organizacion__(self):
        return self.organizacion



# Create your models here.

class Item(models.Model):
    TIPO = (
    ('funcional', 'funcional'),
    ('obsoleto', 'obsoleto'),
    ('perecedero', 'perecedero'),)

    ESTADO=(
    ('presente', 'presente'),
    ('no presente', 'no presente'),
    ('pendiente','pendiente'),)
    id_item = models.AutoField(primary_key=True)
    nombre_item = models.CharField(max_length=150, blank=True)
    fecha_alta_item = models.DateField(null=True, blank=False, auto_now_add=True)
    descripcion_item = models.TextField(max_length=300, blank=True)
    tag_item = models.CharField(max_length=150, blank=True)
    tipo_item = models.CharField(choices=TIPO, blank=True, default='funcional', max_length=150)
    estado_item = models.CharField(choices=ESTADO, blank=True, default='presente', max_length=150)



    def to_json(self):
        return dict(
            id_item=self.id_item,
            nombre_item=self.nombre_item,
            fecha_alta_item=self.fecha_alta_item.isoformat(),
            descripcion_item=self.descripcion_item,
            tag_item=self.tag_item,
            tipo_item=self.tipo_item,
            estado_item=self.estado_item)

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    nombre_inventario = models.CharField(max_length=150, blank=True)
    fecha_alta_inventario = models.DateField(null=True, blank=False, auto_now_add=True)
    descripcion_inventario = models.TextField(max_length=300, blank=True)
    tag_inventario = models.CharField(max_length=150, blank=True)
    caracteristicas_inventario = models.CharField(max_length=300, blank=True)
