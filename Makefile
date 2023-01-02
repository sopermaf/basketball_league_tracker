COMPOSE_FILE := "local.yml"


build:
	docker-compose -f $(COMPOSE_FILE) build

migrate:
	docker-compose -f $(COMPOSE_FILE) run --rm django python manage.py migrate

# ensures all services are running
runserver:
	docker-compose -f $(COMPOSE_FILE) up

make-migration:
	docker-compose -f $(COMPOSE_FILE) run --rm django python manage.py makemigrations

test:
	docker-compose -f $(COMPOSE_FILE) run django pytest --disable-warnings

teardown:
	docker-compose -f $(COMPOSE_FILE) down
