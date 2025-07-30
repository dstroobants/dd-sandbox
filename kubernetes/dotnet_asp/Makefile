#!make
########################################################
## .NET ASP App
########################################################
dotnet-asp-build:
	docker build -t dotnet-asp:latest .
	minikube image load --overwrite dotnet-asp:latest

dotnet-asp-deploy:
	kubectl apply -f dotnet-asp-deployment.yaml
	kubectl apply -f dotnet-asp-service.yaml

dotnet-asp-connect:
	minikube service dotnet-asp

dotnet-asp-delete:
	kubectl delete deployment dotnet-asp
	kubectl delete service dotnet-asp
