#!make
include ../../.env
export

build:
	docker build -t flask-api-dev:latest .
	minikube image load --overwrite flask-api-dev:latest

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

connect:
	minikube service service flask-api

delete:
	kubectl delete deployment flask-api
	kubectl delete service flask-api
