# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
#!/usr/bin/env python




import urllib
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def qrcode(value, alt=None):
    """
    Generate QR Code image from a string with the Google charts API
    Ejemplo de Uso -->  {{ my_string|qrcode:"my alt" }}
    <img src="http://chart.apis.google.com/chart?chs=150x150&amp;cht=qr&amp;chl=my_string&amp;choe=UTF-8" alt="my alt" />
    """
    url = conditional_escape("http://chart.apis.google.com/chart?%s" % \
            urllib.urlencode({'chs':'200x200', 'cht':'qr', 'chl':value, 'choe':'UTF-8'}))
    alt = conditional_escape(alt or value)

    return mark_safe(u"""<img class="qrcode" src="%s" width="200" height="200" alt="%s" />""" % (url, alt))

@register.filter
@stringfilter
def barcode(value, alt=None):
    #{{ my_string|barcode:"my alt" }}#
    url='http://www.mbcestore.com.mx/generador_codigo_de_barras/codigo_de_barras.html?code='+value+'&style=197&type=C128B&width=250&height=50&xres=1&font=4'
    alt = conditional_escape(alt or value)
    return mark_safe(u"""<img class="barcode" style="border-radius: 0px" src="%s"  alt="%s" />""" % (url, alt))


@register.filter("documento_id")
def documento_id(value):
    return str(value['_id'])

@register.filter("unidades")
def unidades(value):
    return str(len(value))

@register.filter("direccion")
def direccion(value):
    aux=value.encode('utf-8')
    aux=aux+', Granada, España'
    print aux
    return aux
