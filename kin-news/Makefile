UUID = 1000

build:
	docker-compose build

run-silent:
	docker-compose up -d

run:
	docker-compose up

tests:
	docker-compose -f docker-compose.test.yaml rm -f postgres redis
	docker-compose -f docker-compose.test.yaml up -d postgres redis
	docker-compose -f docker-compose.test.yaml run --user="root" --rm test-api python manage.py test api/tests/unit
	docker-compose -f docker-compose.test.yaml run --user="root" --rm --no-deps test-api python manage.py test api/tests/integration
	docker-compose -f docker-compose.test.yaml rm -f postgres redis

mypy:
	docker-compose -f docker-compose.test.yaml run -u $(UUID) --rm --no-deps test-api mypy --no-warn-no-return api/

format-check: mypy |
	docker-compose -f docker-compose.test.yaml run -u $(UUID) --rm --no-deps test-api isort --settings-path /app/setup.cfg --check-only api/
	docker-compose -f docker-compose.test.yaml run -u $(UUID) --rm --no-deps test-api flake8 --config /app/setup.cfg api/

format:
	docker-compose run -u $(UUID) --rm --no-deps news-api isort --settings-path /app/setup.cfg api/


ci: format-check | tests

logs:
	docker-compose logs -f 
