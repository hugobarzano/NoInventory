import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NoInventoryProject.settings')
import django
django.setup()
from pymongo import MongoClient

ON_COMPOSE = os.environ.get('COMPOSE')
if ON_COMPOSE:
    client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
else:
    client = MongoClient('mongodb://localhost:27017/')
db = client['noinventory-database']
db2 = client['catalogos-database']

def clearDatabase():
    print "Borrando colecciones"
    db.catalogos.remove()
    db.items.remove()
    print "Colecciones Borradas"

if __name__ == '__main__':
    clearDatabase()
