#!make
########################################################
## Node App
########################################################
node-build:
	docker build --no-cache -t node-app-fastify:latest .
	minikube image load --overwrite node-app-fastify:latest

node-deploy:
	kubectl apply -f node-app-deployment.yaml
	kubectl apply -f node-app-service.yaml

node-connect:
	minikube service node-app-fastify

node-delete:
	kubectl delete deployment node-app-fastify
	kubectl delete service node-app-fastify
