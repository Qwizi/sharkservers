build:
	@echo "Starting building containers"
	docker compose build
	@echo "Containers built"

up:
	@echo "Starting containers"
	docker compose up -d
	@echo "Containers started"

stop:
	@echo "Starting stopping containers"
	docker compose stop
	@echo "Containers stopped"

down:
	@echo "Starting removing containers"
	docker compose down
	@echo "Containers removed"

logs:
	@echo "Starting logs"
	docker compose logs app

uninstall:
	@echo "Starting removing containers"
	docker compose down
	@echo "Containers removed"
	@echo "Started removing instalation file"
	rm -rf src/installed
	@echo "Instalation file removed"


install:
	@echo "Staring database container"
	docker compose up -d
	sleep 2
	docker compose exec app alembic upgrade head
	sleep 2
	@curl -X POST http://localhost:8000/install \
   		-H 'Content-Type: application/json' \
   		-d '{"username":"Qwizi","email":"test@test.pl", "password":"test123456", "password2":"test123456"}'
	@echo "Instalation finished"
test:
	docker compose exec app pytest -vv


generate:
	curl -X GET http://localhost:8000/generate-openapi
	cd ../sharkservers-js-client && npm run generate-client


migration:
	docker compose exec app alembic revision --autogenerate


upgrade:
	docker compose exec app alembic upgrade head


clear-avatars:
	find static/uploads/avatars  -maxdepth 1 -type f ! -name 'index.html' -exec rm -rf {} +

random-data:
	@curl -X GET http://localhost/generate-random-data