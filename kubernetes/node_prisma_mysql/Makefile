#!make
########################################################
## Node App
########################################################
build:
	docker build --no-cache -t node-prisma-app:latest .
	minikube image load --overwrite node-prisma-app:latest

build-deploy: build deploy

deploy-mysql:
	kubectl apply -f mysql-pvc.yaml
	kubectl apply -f mysql-deployment.yaml
	kubectl apply -f mysql-service.yaml

deploy-app:
	kubectl apply -f node-app-deployment.yaml
	kubectl apply -f node-app-service.yaml

deploy: deploy-mysql deploy-app

connect:
	minikube service node-prisma-app

delete-mysql:
	kubectl delete deployment mysql-prisma-app
	kubectl delete service mysql-service
	kubectl delete pvc mysql-pvc

delete-app:
	kubectl delete deployment node-prisma-app
	kubectl delete service node-prisma-app

delete: delete-app delete-mysql delete-minikube-image

delete-minikube-image:
	minikube image rm node-prisma-app:latest
