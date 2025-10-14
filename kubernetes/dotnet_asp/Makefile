#!make
########################################################
## .NET ASP App
########################################################
build:
	docker build -t dotnet-asp:latest .

deploy:
	kubectl apply -f dotnet-asp-deployment.yaml
	kubectl apply -f dotnet-asp-service.yaml

delete:
	kubectl delete deployment dotnet-asp
	kubectl delete service dotnet-asp
