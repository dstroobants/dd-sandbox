#!make
include ../.env
export

build:
	docker build -t flask-api-dev:latest .

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

get-service:
	kubectl get services flask-api

delete:
	kubectl delete deployment flask-api
	kubectl delete service flask-api

build-locally:
	eval $$(minikube docker-env)

build-revert:
	eval $$(minikube docker-env -u)
