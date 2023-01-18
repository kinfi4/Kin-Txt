run-infra:
	docker-compose up -d

run-services:
	cd news-service && make run-silent
	cd statistics-service && make run-silent
	cd kin-news-frontend && make run-silent

run: | run-infra run-services

build:
	cd news-service && make build
	cd statistics-service && make build
	cd kin-news-frontend && make build
