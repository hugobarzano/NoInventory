# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(serialize=False, primary_key=True)),
                ('nombre_inventario', models.CharField(max_length=150, blank=True)),
                ('fecha_alta_inventario', models.DateField(auto_now_add=True, null=True)),
                ('descripcion_inventario', models.TextField(max_length=300, blank=True)),
                ('tag_inventario', models.CharField(max_length=150, blank=True)),
                ('caracteristicas_inventario', models.CharField(max_length=300, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id_item', models.AutoField(serialize=False, primary_key=True)),
                ('nombre_item', models.CharField(max_length=150, blank=True)),
                ('fecha_alta_item', models.DateField(auto_now_add=True, null=True)),
                ('descripcion_item', models.TextField(max_length=300, blank=True)),
                ('tag_item', models.CharField(max_length=150, blank=True)),
                ('tipo_item', models.CharField(default=b'funcional', max_length=150, blank=True, choices=[(b'funcional', b'funcional'), (b'obsoleto', b'obsoleto'), (b'perecedero', b'perecedero')])),
                ('estado_item', models.CharField(default=b'presente', max_length=150, blank=True, choices=[(b'presente', b'presente'), (b'no presente', b'no presente'), (b'pendiente', b'pendiente')])),
            ],
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organizacion', models.CharField(max_length=150, blank=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
