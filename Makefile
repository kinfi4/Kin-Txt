run-infra:
	docker-compose up -d

run-services:
	cd kin-frontend && make run-silent
	cd kin-statistics && make run-silent
	cd kin-news && make run-silent
	cd kin-reports-generation && make run-silent

run: | run-infra run-services

build:
	cd kin-frontend && make build
	cd kin-statistics && make build
	cd kin-news && make build
	cd kin-reports-generation && make build
