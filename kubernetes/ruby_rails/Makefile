#!make
build:
	docker build --no-cache -t rails-app-dev:latest .

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

delete:
	kubectl delete deployment rails-app
	kubectl delete service rails-app
