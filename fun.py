import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NoInventoryProject.settings')
import django
django.setup()
from pymongo import MongoClient


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
