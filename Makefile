build:
	@echo "Starting building containers"
	docker-compose build
	@echo "Containers built"

up:
	@echo "Starting containers"
	docker-compose up -d
	@echo "Containers started"

stop:
	@echo "Starting stopping containers"
	docker-compose stop
	@echo "Containers stopped"

down:
	@echo "Starting removing containers"
	docker-compose down
	@echo "Containers removed"

logs:
	@echo "Starting logs"
	docker-compose logs

uninstall:
	@echo "Starting removing containers"
	docker-compose down
	@echo "Containers removed"
	@echo "Started removing instalation file"
	rm -rf src/installed
	@echo "Instalation file removed"


install:
	@echo "Staring database container"
	docker-compose up -d
	sleep 2
	alembic upgrade head
	sleep 2
	@curl -X POST http://localhost/install \
   		-H 'Content-Type: application/json' \
   		-d '{"username":"Qwizi","email":"test@test.pl", "password":"test123456", "password2":"test123456"}'
	@echo "Instalation finished"
	@curl -X POST http://localhost/v1/players \
   		-H 'Content-Type: application/json' \
   		-d '{"steamid64":"76561198190469450"}'
test:
	docker-compose exec app pytest -vv


generate:
	curl -X GET http://localhost/generate-openapi


migration:
	alembic revision --autogenerate


upgrade:
	alembic upgrade head