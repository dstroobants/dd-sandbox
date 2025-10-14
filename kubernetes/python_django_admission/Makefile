#!make
########################################################
## Datadog Operator
########################################################
# https://docs.datadoghq.com/getting_started/containers/datadog_operator/#installation-and-deployment

# Update helm repositories and install Datadog Operator
DATADOG_API_KEY ?= 
agent-install:
ifndef DATADOG_API_KEY
	$(error DATADOG_API_KEY is required. Usage: make agent-install DATADOG_API_KEY=<your_api_key>)
endif
	helm repo add datadog https://helm.datadoghq.com
	helm repo update
# Check if the operator is already installed and install otherwise
	@if kubectl get deployment datadog-operator >/dev/null 2>&1; then \
		echo "Datadog operator detected, skipping installation"; \
	else \
		echo "Installing Datadog operator"; \
		helm install datadog-operator datadog/datadog-operator; \
	fi
# Create secret with Datadog API Key if it doesn't exist
	@kubectl create secret generic datadog-secret \
		--from-literal api-key=$(DATADOG_API_KEY) \
		--dry-run=client -o yaml | kubectl apply -f -
# Deploy Datadog Agent
	kubectl apply -f datadog-agent.yaml

# Upgrade Datadog Operator with new values
agent-upgrade:
	kubectl apply -f datadog-agent.yaml

agent-delete:
	kubectl delete datadogagent datadog
	helm delete datadog-operator

########################################################
## Django App
########################################################
build:
	docker build --no-cache -t django-app:latest .

deploy:
	kubectl apply -f django-app-deployment.yaml
	kubectl apply -f django-app-service.yaml

delete:
	kubectl delete deployment django-app
	kubectl delete service django-app
