#!make
########################################################
## PHP Laravel React App
########################################################
build:
	docker build --no-cache -t php-laravel-react:latest .

deploy:
	kubectl -n dev apply -f php-laravel-deployment.yaml
	kubectl -n dev apply -f php-laravel-service.yaml

delete:
	kubectl -n dev delete deployment php-laravel
	kubectl -n dev delete service php-laravel
