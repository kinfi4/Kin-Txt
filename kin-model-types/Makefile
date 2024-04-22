UUID = 1000

build:
	docker compose build

run-silent:
	docker compose up -d

run:
	docker compose up

mypy:
	docker compose run -u $(UUID) --rm --no-deps model-types-api mypy kin_model_types/

tests:
	docker compose -f docker-compose.test.yaml run --user "root" --rm --no-deps model-types coverage run -a -m pytest -vv -s

silent-tests: 
	docker compose -f docker-compose.test.yaml run --user "root" --rm --no-deps model-types coverage run -m pytest -v -q --log-cli-level=CRITICAL

logs:
	docker compose logs -f 

restart:
	docker compose stop
	docker compose up -d 

make-migrations:
	docker compose run --rm --no-deps model-types-api alembic revision --autogenerate -m "New migration"
