#!make
########################################################
## PHP Laravel React App
########################################################
php-build:
	docker build --no-cache -t php-laravel-react:latest .
	minikube image load --overwrite php-laravel-react:latest

php-deploy:
	kubectl apply -f php-laravel-deployment.yaml
	kubectl apply -f php-laravel-service.yaml

php-connect:
	minikube service php-laravel

php-delete:
	kubectl delete deployment php-laravel
	kubectl delete service php-laravel
