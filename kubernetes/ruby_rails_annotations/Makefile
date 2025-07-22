#!make
include ../../.env
export

build-rails-app:
	rbenv install 3.3.8
	rbenv local  3.3.8

	# Verify Ruby version
	ruby -v

	# Install Rails gem for this Ruby version
	sudo gem install rails

	# Create new Rails app
	rails new my_rails_app

build:
	docker build --no-cache -t rails-app-dev:latest .
	minikube image load rails-app-dev:latest

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

get-service:
	minikube service rails-app

delete:
	kubectl delete deployment rails-app
	kubectl delete service rails-app
