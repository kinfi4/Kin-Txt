run-infra:
	docker compose up -d

run-services:
	cd kin-frontend && make run-silent
	cd kin-statistics && make run-silent
	cd kin-news && make run-silent
	cd kin-generic-reports-builder && make run-silent
	cd kin-api-gateway && make run-silent
	cd kin-model-types && make run-silent

run: | run-infra run-services

build:
	cd kin-frontend && make build
	cd kin-statistics && make build
	cd kin-news && make build
	cd kin-generic-reports-builder && make build
	cd kin-api-gateway && make build
	cd kin-model-types && make build 
	cd kin-news-classification-reports-builder && make build
