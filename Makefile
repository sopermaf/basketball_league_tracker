# set environment variable to `production.yml` for releasing
COMPOSE_FILE ?= "docker-compose.local.yml"

build:
	docker-compose -f $(COMPOSE_FILE) build

teardown:
	docker-compose -f $(COMPOSE_FILE) down

stop:
	docker-compose -f $(COMPOSE_FILE) stop

update-running: build stop migrate
	docker-compose -f $(COMPOSE_FILE) up -d

logs-follow:
	docker-compose -f $(COMPOSE_FILE) logs -f $(container)

# ensures all services are running first but equivalent to runserver
runserver:
	docker-compose -f $(COMPOSE_FILE) up

# run any django manage.py command
django-%:
	docker-compose -f $(COMPOSE_FILE) run --rm django python manage.py $* $(args)


# selection of commonly used django-admin commands to make autocomplete easier
migrate:
	$(MAKE) django-migrate

makemigrations:
	$(MAKE) django-makemigrations

shell:
	$(MAKE) django-shell_plus

test:
	docker-compose -f $(COMPOSE_FILE) run django pytest --disable-warnings
