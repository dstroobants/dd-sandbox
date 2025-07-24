#!make
include ../../.env
export

build:
	docker build -t rails-app-dev:latest .
	minikube image load --overwrite rails-app-dev:latest

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

get-service:
	kubectl get service rails-app

delete:
	kubectl delete deployment rails-app
	kubectl delete service rails-app
