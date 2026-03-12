#!make
########################################################
## .NET ASP App
########################################################
build:
	docker build -t dotnet-asp:latest .

deploy:
	kubectl -n dev apply -f dotnet-asp-deployment.yaml
	kubectl -n dev apply -f dotnet-asp-service.yaml

delete:
	kubectl -n dev delete deployment dotnet-asp
	kubectl -n dev delete service dotnet-asp
