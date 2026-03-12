#!make
build:
	docker build --no-cache -t rails-app-dev:latest .

deploy:
	kubectl -n dev apply -f deployment.yaml
	kubectl -n dev apply -f service.yaml

delete:
	kubectl -n dev delete deployment rails-app
	kubectl -n dev delete service rails-app
