#!make
########################################################
## PHP Laravel React App
########################################################
build:
	docker build --no-cache -t php-laravel-react:latest .

deploy:
	kubectl apply -f php-laravel-deployment.yaml
	kubectl apply -f php-laravel-service.yaml

delete:
	kubectl delete deployment php-laravel
	kubectl delete service php-laravel
