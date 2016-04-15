# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
import csv
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import StringIO
import time
from bson import ObjectId
from django.http import HttpResponse
from django.http import HttpResponseServerError
from NoInventory.forms import *
from NoInventory.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from bson.json_util import dumps
import json
import os
from item import *
from catalogo import *
from clasificacion import *
from io import StringIO



gestorItems = ItemsDriver()
gestorCatalogos = CatalogosDriver()
gestorClasificacion=ClasificacionDriver()



from pymongo import MongoClient

ON_COMPOSE = os.environ.get('COMPOSE')
if ON_COMPOSE:
    client = MongoClient('mongodb://172.17.0.2:27017/')
else:
    client = MongoClient('mongodb://localhost:27017/')
db = client['noinventory-database']
#os.environ['DB_PORT_27017_TCP_ADDR']


########################### VISTAS PRINCIPALES #################################
def index(request):
    #print "variable entorno:"
    #print VAR
    #return redirect('/noinventory/index/')
    return render(request, 'noinventory/index.html')

@csrf_exempt
def items(request):

        lista_items=gestorItems.database.items.find({"usuario":request.session['username']})
        contexto = {"lista_items":lista_items}
        return render(request, 'noinventory/items.html',contexto)

def prueba(request):
    lista_items=gestorItems.database.items.find({"usuario":request.session['username']})
    form = SelectItem()
    return render(request, 'noinventory/prueba.html', {'form': form,"lista_items":lista_items})

@csrf_exempt
def catalogos(request):
    lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.session['username']})
    contexto = {"lista_catalogos":lista_catalogos}
    return render(request, 'noinventory/catalogos.html',contexto)

@csrf_exempt
def catalogo(request,id_catalogo):
    catalogo_object=Catalogo()

    lista_items=gestorItems.database.items.find({"usuario":request.session['username']})
    catalogo=gestorCatalogos.read(catalogo_id=id_catalogo)
    for i in catalogo:
        catalogo_object = Catalogo.build_from_json(i)

    for j in catalogo_object.items_catalogo:
        print j

    contexto = {"catalogo":catalogo_object,"catalogo_id":id_catalogo,"lista_items":lista_items}
    return render(request, 'noinventory/catalogo.html',contexto)



@csrf_exempt
def addToCatalogo(request,id_catalogo,id_item):
        gestorCatalogos.addToCatalogo(id_catalogo,id_item,gestorItems)
        lista_items=gestorItems.read()
        catalogo=gestorCatalogos.read(catalogo_id=id_catalogo)
        catalogo_object=Catalogo()
        for i in catalogo:
            catalogo_object = Catalogo.build_from_json(i)
        contexto = {"catalogo":catalogo_object,"catalogo_id":id_catalogo,"lista_items":lista_items}
        return redirect('/noinventory/catalogo/'+id_catalogo,contexto)




############################ ADMINISTRACION DE PREFERENCIAS ##########################

class Preferencias(View):

    def get(self, request):
        print "Entrando por el get"
        form=FormEntrada()
        return render(request, 'noinventory/preferencias.html', {'form': form})

    def post(self, request):
        print "Entrando por el post"
        reader_tag1=None
        reader_tag2=None
        reader_tag3=None
        form = FormEntrada(request.POST, request.FILES)
        if form.is_valid():
        #print "formulario valido"
            ##Frichero 1
            fichero1=request.FILES.get('file_tag1',None)
            if fichero1 is not None:
                fieldnames = ("CLAVE1","VALOR1")
                reader_tag1 = csv.DictReader(request.FILES['file_tag1'], fieldnames)
                if reader_tag1 is None:
                    gestorClasificacion.createDefaultTag1(request.session['organizacion'])
                else:
                    gestorClasificacion.createTag1FromReader(reader_tag1,request.session['organizacion'])
            else:
                gestorClasificacion.createDefaultTag1(request.session['organizacion'])

            ##Fichero 2
            fichero2=request.FILES.get('file_tag2',None)
            if fichero2 is not None:
                fieldnames = ("CLAVE2","VALOR2")
                reader_tag2 = csv.DictReader(request.FILES['file_tag2'], fieldnames)
                if reader_tag2 is None:
                    gestorClasificacion.createDefaultTag2(request.session['organizacion'])
                else:
                    gestorClasificacion.createTag2FromReader(reader_tag2,request.session['organizacion'])
            else:
                gestorClasificacion.createDefaultTag2(request.session['organizacion'])
            #Fichero 3
            fichero3=request.FILES.get('file_tag3',None)
            if fichero3 is not None:
                fieldnames = ("CLAVE3","VALOR3")
                reader_tag3 = csv.DictReader(request.FILES['file_tag3'], fieldnames)
                if reader_tag3 is None:
                    gestorClasificacion.createDefaultTag3(request.session['organizacion'])
                else:
                    gestorClasificacion.createTag3FromReader(reader_tag3,request.session['organizacion'])
            else:
                gestorClasificacion.createDefaultTag3(request.session['organizacion'])
            return redirect('/noinventory/preferencias',{'form':form})
        else:
            print "formulario invalido"
            #form = FormEntrada()
            return render(request, 'noinventory/preferencias.html', {'form': form})


def deleteItems(request):
    gestorItems.destroyDriver()
    return redirect('/noinventory/preferencias')

def deleteInventorys(request):
    gestorCatalogos.destroyDriver()
    return redirect('/noinventory/preferencias')


########################### VISTAS JSON PARA ANDROID ################################
@csrf_exempt
def catalogosJson(request):
    if request.method == 'GET':

        return HttpResponse("catalogos json")
    else:
        default={"_id":"ID","nombre":"Nombre","descripcion":"Descripcion"}
        aux7=[]
        aux7.append(default)
        respuesta={"catalogos":aux7}
        aux=[]
        aux3=[]
        if request.POST["flag"] == "True":
            try:
                lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.POST["username"]})
                for i in lista_catalogos:
                    aux = Catalogo.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_catalogo"],"descripcion":aux2["descripcion_catalogo"]}
                    aux3.append(aux4)
                    respuesta={"catalogos":aux3}
            except KeyError as e:
                raise Exception("No tienes catalogos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)
        else:

            try:
                lista_catalogos=gestorCatalogos.database.catalogos.find({"organizacion":request.POST["organizacion"]})
                for i in lista_items:
                    aux = Catalogo.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_catalogo"],"descripcion":aux2["descripcion_catalogo"]}
                    aux3.append(aux4)
                    respuesta={"catalogos":aux3}
            except KeyError as e:
                raise Exception("Organizacion sin  objetos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)

@csrf_exempt
def itemsJson(request):
    if request.method == 'GET':

        return HttpResponse()
    else:
        default={"_id":"ID","nombre":"Nombre","descripcion":"Descripcion"}
        aux7=[]
        aux7.append(default)
        respuesta={"items":aux7}
        aux=[]
        aux3=[]
        if request.POST["flag"] == "True":

            try:
                lista_items=gestorItems.database.items.find({"usuario":request.POST["username"]})
                for i in lista_items:
                    aux = Item.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_item"],"descripcion":aux2["descripcion_item"]}
                    aux3.append(aux4)
                    respuesta={"items":aux3}
            except KeyError as e:
                raise Exception("No tienes objetos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)
        else:

            try:
                lista_items=gestorItems.database.items.find({"organizacion":request.POST["organizacion"]})
                for i in lista_items:
                    aux = Item.build_from_json(i)
                    aux2=aux.get_as_json()
                    aux2["_id"]=str(aux2["_id"])
                    aux4={"_id":aux2["_id"],"nombre":aux2["nombre_item"],"descripcion":aux2["descripcion_item"]}
                    aux3.append(aux4)
                    respuesta={"items":aux3}
            except KeyError as e:
                raise Exception("Organizacion sin  objetos asociados : {}".format(e.message))
            return JsonResponse(respuesta,safe=False)


@csrf_exempt
def itemJson(request):
    if request.method == 'GET':
        return HttpResponse("get response")
    else:
        respuesta={""}
        print request.POST["item_id"]
        try:
            lista_items=gestorItems.database.items.find({"_id":ObjectId(request.POST["item_id"])})
            for i in lista_items:
                aux = Item.build_from_json(i)
                aux2=aux.get_as_json()
                aux2["_id"]=str(aux2["_id"])
                respuesta={"_id":aux2["_id"],"nombre":aux2["nombre_item"],"descripcion":aux2["descripcion_item"],"localizador":aux2["localizador"]}
                #aux2=str(respuesta)
                print respuesta
        except KeyError as e:
            raise Exception("No existe objeto : {}".format(e.message))
        return JsonResponse(respuesta,safe=False)

@csrf_exempt
def addItemFromQr(request):
    if request.method == 'POST':
        #print "Dicionario completo"

        mydic=dict(request.POST)

        catalogo=mydic["catalogo"]
        #print "catalogo:"
        #print catalogo[0]
        aux=mydic["scaner"][0]
        #print aux
        buscar = "\'"
        reemplazar_por = "\""
        b=aux.replace(buscar, reemplazar_por)
        #print b
        data_aux=json.loads(b)
        #print data_aux["_id"]
        #print data_aux["fecha_alta_item"]
        #gestorCatalogos.addToCatalogo(mydic["catalogo"],ObjectId(data_aux["_id"]),gestorItems)
        item=gestorItems.read(item_id=data_aux["_id"])
        if item is not None:
            for i in item:
                #print "entra forrrr"
                item_object = Item.build_from_json(i)
        else:
            raise Exception("Item no valido para add")
        #print "Item\n"
        #print item_object.nombre_item

        catalogo=gestorCatalogos.read(catalogo_id=catalogo[0])
        if catalogo is not None:
            for i in catalogo:
                #print "entra forrrr 2"
                catalogo_object = Catalogo.build_from_json(i)
        else:
            raise Exception("Catalogo no valido para add")
        #print "Catalogo\n"
        #print catalogo_object.nombre_catalogo

        #gestorCatalogos.addToCatalogo(catalogo[0],data_aux["_id"],gestorItems)
        gestorCatalogos.database.catalogos.update({"_id": catalogo_object._id},{"$addToSet": {"items_catalogo" : item_object.nombre_item,}})
        return HttpResponse("OK")

    else:
        print "recibido get"
    #    print request.GET['contenido_scaner']
        return HttpResponse("gettttttt")




class AndroidItemCreator(View):
    organizacion=None
    def get(self, request):
        form = ItemForm3(organizacion=request.GET['organizacion'])
        #print request.GET['organizacion']
        #form = ItemForm3(organizacion=request.GET['organizacion'])
        return render(request, 'noinventory/nuevoItem.html', {'form': form})

    def post(self, request):
        form = ItemForm3(request.POST,organizacion=request.GET['organizacion'])
        if form.is_valid():
            item =Item.build_from_json({"nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": time.strftime("%c"),
                        "descripcion_item": form.data['descripcion_item'],
                        "organizacion":request.GET['organizacion'],
                        "usuario":request.GET['organizacion'],
                        "tag1": form.data['tag1'],
                        "tag2": form.data['tag2'],
                        "tag3": form.data['tag3'],
                        "localizador":" ",
                        "qr_data":" ",
                        })
            gestorItems.create(item,gestorClasificacion,request.GET['organizacion'])
            lista_items=gestorItems.read()
            contexto = {"lista_items":lista_items}
            return redirect('/noinventory/items',contexto)
        else:
            return render(request, 'noinventory/nuevoItem.html', {'form': form})






################################## COSAS VARIAS ########################################
def jsonTOstring(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Item:" + elemento["nombre_item"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_item"]+"\nDescripcion:"+elemento["descripcion_item"]+"\nEstado:"+elemento["estado_item"]+"\nTipo:"+elemento["tipo_item"]+"\nTags:"+elemento["organizacion"]
    return texto


def jsonTOstringCatalogo(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Catalogo:" + elemento["nombre_catalogo"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_catalogo"]+"\nDescripcion:"+elemento["descripcion_catalogo"]+"\nTags:"+elemento["tag_catalogo"]
    return texto

def desplegable():
    tupla= []
    tupla2=[]
    aux2 = []
    aux4 = []
    lista_items=[]
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
    return SEL2


######################### GESTION DE ITEMS y CATALOGOS #######################
@csrf_exempt
def borrarItem(request):
    i_id = None
    print "vamos a borrar"
    if request.method == 'GET':
        default={"_id":"ID","nombre":"Nombre","descripcion":"Descripcion"}
        aux7=[]
        aux7.append(default)
        respuesta={"items":aux7}
        aux=[]
        aux3=[]
        i_id = request.GET['id_item']
        print i_id
        gestorItems.database.items.remove( {"_id" : ObjectId(i_id) } )
        print "Borrado completado"
        try:
            #lista_items=gestorItems.database.items.find({"usuario":request.session["username"]})
            lista_items=gestorItems.database.items.find({"usuario":request.session["username"]})
            for i in lista_items:
                aux = Item.build_from_json(i)
                aux2=aux.get_as_json()
                aux2["_id"]=str(aux2["_id"])
                #aux4={"_id":aux2["_id"],"nombre":aux2["nombre_item"],"descripcion":aux2["descripcion_item"]}
                aux3.append(aux2)
                respuesta={"items":aux3}
        except KeyError as e:
            raise Exception("No tienes objetos asociados : {}".format(e.message))
        print "Respuestad del servidor"
        print respuesta
        return JsonResponse(respuesta,safe=False)



class ItemCreator(View):

    def get(self, request):
        form = ItemForm3(organizacion=request.session['organizacion'])
        #print request.GET['organizacion']
        #form = ItemForm3(organizacion=request.GET['organizacion'])
        return render(request, 'noinventory/nuevoItem.html', {'form': form})

    def post(self, request):
        form = ItemForm3(request.POST,organizacion=request.session['organizacion'])
        if form.is_valid():
            item =Item.build_from_json({"nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": time.strftime("%c"),
                        "descripcion_item": form.data['descripcion_item'],
                        "organizacion": request.session["organizacion"],
                        "usuario":request.session['username'],
                        "tag1": form.data['tag1'],
                        "tag2": form.data['tag2'],
                        "tag3": form.data['tag3'],
                        "localizador":" ",
                        "qr_data":" ",
                        })
            gestorItems.create(item,gestorClasificacion,request.session['organizacion'])
            lista_items=gestorItems.database.items.find({"usuario":request.session["username"]})
            contexto = {"lista_items":lista_items}
            return redirect('/noinventory/items',contexto)
        else:
            return render(request, 'noinventory/nuevoItem.html', {'form': form})


class ItemUpdater(View):

    def get(self, request,id_item):
        cursor=gestorItems.read(item_id=id_item)
        for i in cursor:
            currentItem = Item.build_from_json(i)

        aux=currentItem.get_as_json()
        print aux
        form = ItemForm3(aux,organizacion=request.session['organizacion'])
        form.data["descripcion_item"]=str(form.data["descripcion_item"])+"\nUltima modificacion: "+time.strftime("%c")
        #form.data["tag1"]=aux["tag1"]
        return render(request, 'noinventory/modificarItem.html', {'form': form,'id_item':currentItem._id})

    def post(self, request,id_item):
        cursor=gestorItems.read(item_id=id_item)
        for i in cursor:
            c = Item.build_from_json(i)
        form = ItemForm3(request.POST,organizacion=request.session['organizacion'])
        if form.is_valid():
            tag1=gestorClasificacion.database.tag1.find_one({"VALOR1":form.data["tag1"]})
            itemUpdated =Item.build_from_json({"_id":c._id,
                        "nombre_item": form.data['nombre_item'],
                        "fecha_alta_item": c.fecha_alta_item,
                        "descripcion_item": form.data['descripcion_item'],
                        "organizacion": c.organizacion,
                        "usuario":c.usuario,
                        "tag1":form.data["tag1"],
                        "tag2": form.data['tag2'],
                        "tag3": form.data['tag3'],
                        "localizador":c.localizador,
                        "qr_data":c.qr_data,
                        })
            gestorItems.update(itemUpdated,gestorClasificacion,request.session['organizacion'])
            lista_items=gestorItems.database.items.find({"usuario":request.session["username"]})
            contexto = {"lista_items":lista_items}
            return redirect('/noinventory/items',contexto)
        else:
            print form.errors
            return render(request, 'noinventory/modificarItem.html', {'form': form,'id_item':id_item})

class CatalogoCreator(View):

    def get(self, request):
        form = CatalogoForm()
        return render(request, 'noinventory/nuevoCatalogo.html', {'form': form})

    def post(self, request):
        form = CatalogoForm(request.POST)
        if form.is_valid():
            catalogo =Catalogo.build_from_json({"nombre_catalogo": form.data['nombre_catalogo'],
                        "fecha_alta_catalogo": time.strftime("%c"),
                        "descripcion_catalogo": form.data['descripcion_catalogo'],
                        "organizacion": request.session["organizacion"],
                        "usuario":request.session['username'],
                        "tag_catalogo": form.data['tag_catalogo'],
                        "tipo_catalogo":form.data['tipo_catalogo'],
                        "items_catalogo": [],
                        "qr_data":" ",
                        })
            gestorCatalogos.create(catalogo)
            lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.session["username"]})
            contexto = {"lista_catalogos":lista_catalogos}
            return redirect('/noinventory/catalogos',contexto)
        else:
            print form.errors
            return render(request, 'noinventory/nuevoCatalogo.html', {'form': form})


class CatalogoUpdater(View):

    def get(self, request,id_catalogo):
        cursor=gestorCatalogos.read(catalogo_id=id_catalogo)
        currentcatalogo=Catalogo()
        for i in cursor:
            currentcatalogo = Catalogo.build_from_json(i)
        aux=currentcatalogo.get_as_json()
        form = CatalogoForm(aux)
        form.data["descripcion_catalogo"]=str(form.data["descripcion_catalogo"])+"\nUltima modificacion: "+time.strftime("%c")
        return render(request, 'noinventory/modificarCatalogo.html', {'form': form,'id_catalogo':currentcatalogo._id})

    def post(self, request,id_catalogo):
        cursor=gestorCatalogos.read(catalogo_id=id_catalogo)
        for i in cursor:
            c = Catalogo.build_from_json(i)
        form = CatalogoForm(request.POST)
        if form.is_valid():
            catalogoUpdated =Catalogo.build_from_json({"_id":c._id,
                        "nombre_catalogo": form.data['nombre_catalogo'],
                        "fecha_alta_catalogo": c.fecha_alta_catalogo,
                        "descripcion_catalogo": form.data['descripcion_catalogo'],
                        "organizacion": c.organizacion,
                        "usuario":c.usuario,
                        "tag_catalogo": form.data['tag_catalogo'],
                        "tipo_catalogo": form.data['tipo_catalogo'],
                        "items_catalogo": c.items_catalogo,
                        "qr_data":c.qr_data,
                        })
            gestorCatalogos.update(catalogoUpdated)
            lista_catalogos=gestorCatalogos.database.catalogos.find({"usuario":request.session["username"]})
            contexto = {"lista_catalogos":lista_catalogos}
            return redirect('/noinventory/catalogo/'+str(c._id),contexto)
        else:
            return render(request, 'noinventory/modificarCatalogo.html', {'form': form,'id_catalogo':id_catalogo})




######################### REGISTRO DE USUARIOS ############################################

@csrf_exempt
def androidLogin(request):
    if request.method=='POST':

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                u=User.objects.get(username=user.username)
                user_profile = UserProfile.objects.get(user=user)
                login(request, user)
                #data="nombre_usuario :"+username
                return HttpResponse(user_profile.__organizacion__())
            else:
                return HttpResponse("Your No-Inventory account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        print "entrando por get"
    return HttpResponse()


@csrf_exempt
def androidRegister(request):
    if request.method=='POST':
        #print request.POST["username"]
        #print request.POST["email"]
         #print request.POST["password"]
        #print request.POST["organizacion"]

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid():
            if profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return HttpResponse("success")
            else:
                return HttpResponse("Invalid User or Organizacion")
        else:
            return HttpResponse("Username exist or Invalid Email")
    else:
        print "entrando por get"
    return HttpResponse()


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            return HttpResponseRedirect('/noinventory/')
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            return redirect('registration/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

            #print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'registration/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                u=User.objects.get(username=user.username)
                request.session['username'] = u.username
                user_profile = UserProfile.objects.get(user=user)
                #print user_profile.__organizacion__()
                request.session['organizacion'] = user_profile.__organizacion__()
                login(request, user)
                return HttpResponseRedirect('/noinventory/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your No-Inventory account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'registration/login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    del request.session['username']
    del request.session['organizacion']
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/noinventory/')
