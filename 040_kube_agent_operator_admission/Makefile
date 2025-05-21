#!make
include ../.env
export

# Update helm repositories
update:
	helm repo add datadog https://helm.datadoghq.com
	helm repo update

# Install Datadog Operator
# Create secret with Datadog API and APP keys
# Apply Datadog operator/agent configuration
install:
	@if ! helm list -q | grep -q "^datadog-operator$$"; then \
		helm install datadog-operator datadog/datadog-operator; \
	fi
	@if ! kubectl get secret datadog-secret >/dev/null 2>&1; then \
		kubectl create secret generic datadog-secret \
			--from-literal api-key=${DD_API_KEY} \
			--from-literal app-key=${DD_APP_KEY}; \
	fi
	kubectl apply -f datadog-agent.yaml

# Upgrade Datadog Operator with new values
upgrade:
	kubectl apply -f datadog-agent.yaml

delete:
	kubectl delete datadogagent datadog
	helm delete datadog-operator
