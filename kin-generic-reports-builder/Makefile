UUID = 1000

build:
	docker compose build

run-silent:
	docker compose up -d

run:
	docker compose up

logs:
	docker compose logs -f 

restart:
	docker compose stop
	docker compose up -d 

mypy:
	docker compose run --rm generic-builder-consumer mypy kin_generic_builder
