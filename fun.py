import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NoInventoryProject.settings')
import django
django.setup()
from pymongo import MongoClient

ON_COMPOSE = os.environ.get('COMPOSE')
if ON_COMPOSE:
    client = MongoClient('mongodb://db:27017/')
else:
    client = MongoClient('mongodb://localhost:27017/')
db = client['noinventory-database']
db2 = client['inventarios-database']

def clearDatabase():
    print "Borrando colecciones"
    db.inventarios.remove()
    db.items.remove()
    print "Colecciones Borradas"

if __name__ == '__main__':
    clearDatabase()
