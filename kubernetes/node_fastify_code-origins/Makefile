#!make
########################################################
## Node App
########################################################
build:
	docker build --no-cache -t node-app-fastify:latest .

deploy:
	kubectl apply -f node-app-deployment.yaml
	kubectl apply -f node-app-service.yaml

delete:
	kubectl delete deployment node-app-fastify
	kubectl delete service node-app-fastify
