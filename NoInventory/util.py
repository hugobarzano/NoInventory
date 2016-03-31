organizacion_global=None

def setOrganizacion(organizacion):
    global organizacion_global
    organizacion_global=organizacion

def getOrganizacion():
    global organizacion_global
    return organizacion_global
