# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
from bson.objectid import ObjectId
#from pymongo.objectid import ObjectId
from pymongo import *
import time
from django.conf import settings
import os

from django.conf import settings
import os

from item import *





def main():
    manejador = ItemsDriver()

    #manejardor3= CatalogosDriver()
    #manejardor3.database.catalogos.remove()
    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS"
    print "#######################################################\n"





    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA ITEMS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
