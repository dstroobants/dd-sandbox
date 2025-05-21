#!make
include ../.env
export

build:
	docker build -t ${DOCKER_USERNAME}/flask-api-dev:latest .

push:
	docker push ${DOCKER_USERNAME}/flask-api-dev:latest

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

get-service:
	kubectl get services flask-api-service

delete:
	kubectl delete deployment flask-api-deployment
	kubectl delete service flask-api-service
