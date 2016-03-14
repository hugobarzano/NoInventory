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

docker:
	sudo service docker restart
	sudo docker build -f Dockerfile -t aplicacion --no-cache=true .
	sudo docker run -t -p 80:80 -i aplicacion sh -c "sudo service mongodb restart && ifconfig && cd /NoInventory &&  python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py syncdb --noinput && sudo python manage.py runserver 0.0.0.0:80"
docker_compose:
		sudo service docker restart
		sudo docker pull sameersbn/mongodb:latest
		sudo docker pull hugobarzano/noinventory:latest
		sudo docker-compose up
		echo Voy a esperar 10 segundos a la base de datos
		sleep 10
		sudo docker-compose run web
