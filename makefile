#Makefile
install:
	sudo chmod +x install.sh
	sudo ./install.sh

inicializar:
		python manage.py makemigrations --noinput
		python manage.py migrate --noinput
		python manage.py syncdb --noinput
		sudo service mongodb restart

free:
	sudo fuser -k 80/tcp

run:
	sudo python manage.py runserver 0.0.0.0:80

test_item:
	python NoInventory/test_item.py

test_inventory:
	python NoInventory/test_inventario.py
