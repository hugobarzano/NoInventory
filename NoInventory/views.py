from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import time
from bson import ObjectId
from django.http import HttpResponse
from NoInventory.forms import *
from django.http import HttpResponseRedirect

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['items-database']
db2 = client['inventarios-database']
items=db.items
inventarios=db2.inventarios

def index(request):
    lista_items=db.items.find()
    contexto = {"lista_items":lista_items}
    return render(request, 'noinventory/index.html',contexto)

def items(request):
    lista_items=db.items.find()
    contexto = {"lista_items":lista_items}
    return render(request, 'noinventory/items.html',contexto)

def prueba(request):
    form = SelectItem()
    return render(request, 'noinventory/prueba.html', {'form': form})

def inventarios(request):
    lista_inventarios=db2.inventarios.find()
    contexto = {"lista_inventarios":lista_inventarios}
    return render(request, 'noinventory/inventarios.html',contexto)


@csrf_exempt
def inventario2(request,id_inventario):
    nombre_items=[]
    inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
    print "inventario Despues de insertar:"
    print inventario["items_inventario"]
    for i in inventario["items_inventario"]:
        item=db.items.find_one({"_id": i})
        nombre_items.append(item["nombre_item"])
    print nombre_items

    inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
    lista_items=db.items.find()
    form = SelectItem()
    contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
    return render(request, 'noinventory/inventario.html', contexto)




@csrf_exempt
def inventario(request,id_inventario):
    nombre_items=[]
    if request.method == 'POST':
        form = SelectItem(request.POST)
        if form.is_valid():
            print "formulario nombre:"
            print form.data["items"]
            item=db.items.find_one({"nombre_item": form.data["items"]})
            inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
            db2.inventarios.update({"_id": ObjectId(id_inventario)},{"$push": {"items_inventario" :  item["_id"],}})
            inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
            print "inventario Despues de insertar:"
            print inventario["items_inventario"]
            for i in inventario["items_inventario"]:
                item=db.items.find_one({"_id": i})
                nombre_items.append(item["nombre_item"])
            print nombre_items
            lista_items=db.items.find()
            contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
            return render(request, 'noinventory/inventario.html',contexto)
        else:
            print form.errors
    else:
        inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
        form = SelectItem()
        lista_items=db.items.find()
        contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
    return render(request, 'noinventory/inventario.html', contexto)


@csrf_exempt
def addToInventario(request,id_inventario,id_item):
        item=db.items.find_one({"_id": ObjectId(id_item)})
        inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
        db2.inventarios.update({"_id": ObjectId(id_inventario)},{"$addToSet": {"items_inventario" :  item["_id"],}})
        inventario=db2.inventarios.find_one({"_id": ObjectId(id_inventario)})
        form = SelectItem()
        lista_items=db.items.find()
        contexto = {"inventario":inventario,"lista_items":lista_items,"form": form}
        return render(request, 'noinventory/inventario.html', contexto)

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
            id_item=db.items.insert(item)
            #print id_item
            qr_data_generated=jsonTOstring(db.items.find_one({"_id": id_item}))
            #print qr_data_generated
            db.items.update_one({"_id":id_item},{"$set": {"qr_data": qr_data_generated}})
            lista_items=db.items.find()
            #print lista_items
            #for i in lista_items:
                #print i
            contexto = {"lista_items":lista_items}
            return render(request, 'noinventory/items.html',contexto)
        else:
            print form.errors
    else:
        form = ItemForm()
    return render(request, 'noinventory/nuevoItem.html', {'form': form})

def jsonTOstring(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Item:" + elemento["nombre_item"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_item"]+"\nDescripcion:"+elemento["descripcion_item"]+"\nEstado:"+elemento["estado_item"]+"\nTipo:"+elemento["tipo_item"]+"\nTags:"+elemento["tag_item"]
    return texto


@csrf_exempt
def nuevoInventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            inventario = {    "nombre_inventario": form.data['nombre_inventario'],
                        "fecha_alta_inventario": time.strftime("%c"),
                        "descripcion_inventario": form.data['descripcion_inventario'],
                        "tag_inventario": form.data['tag_inventario'],
                        "caracteristicas_inventario":form.data['caracteristicas_inventario'],
                        "items_inventario": []
                        }
            id_inventario=db2.inventarios.insert(inventario)
            #print id_item
            qr_data_generated=jsonTOstringInventario(db2.inventarios.find_one({"_id": id_inventario}))
            #print qr_data_generated
            db2.inventarios.update_one({"_id":id_inventario},{"$set": {"qr_data": qr_data_generated}})
            lista_inventarios=db2.inventarios.find()
            #print lista_items
            #for i in lista_items:
                #print i
            contexto = {"lista_inventarios":lista_inventarios}
            return render(request, 'noinventory/inventarios.html',contexto)
        else:
            print form.errors
    else:
        form = InventarioForm()
    return render(request, 'noinventory/nuevoInventario.html', {'form': form})


def jsonTOstringInventario(elemento):
    #d=json.dumps(elemento)
    texto="Nombre Inventario:" + elemento["nombre_inventario"] + "\nIdentificador:"+str(elemento["_id"]) + "\nFecha de Alta:"+elemento["fecha_alta_inventario"]+"\nDescripcion:"+elemento["descripcion_inventario"]+"\nTags:"+elemento["tag_inventario"]
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




def registro(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UsuarioForm(data=request.POST)
        profile_form = PerfilUsuarioForm(data=request.POST)

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

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UsuarioForm()
        profile_form = PerfilUsuarioForm()

    # Render the template depending on the context.
    return render(request,'noinventory/registro.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
