import csv
import json
from pymongo import MongoClient
import os


ON_COMPOSE = os.environ.get('COMPOSE')
if ON_COMPOSE:
    client = MongoClient('mongodb://db:27017/')
else:
    client = MongoClient('mongodb://localhost:27017/')
db = client['noinventory-database']



def csvTOjson():
    csvfile = open('Codigo_Centro.csv', 'r')
    jsonfile = open('file.json', 'w')
    fieldnames = ("COD_ENTIDAD","ENTIDAD")
    reader = csv.DictReader( csvfile, fieldnames)
    for row in reader:
        print row
        json.dump(row, jsonfile)
        jsonfile.write('\n')

def csvTOmongo():
    csvfile = open('Codigo_Centro.csv', 'r')
    fieldnames = ("COD_ENTIDAD","ENTIDAD")
    reader = csv.DictReader( csvfile, fieldnames)
    for row in reader:
        db.entidades.insert(row)



if __name__ == '__main__':
    print "Convirtiendo a Json"
    #csvTOjson()
    csvTOmongo()
    ent=db.entidades.find()
    for i in ent:
        print i
