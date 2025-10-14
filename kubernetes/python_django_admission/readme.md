
# Intro
Django application using a Gunicorn server.
The application itself is just boilerplate AI-generated code that mostly works and located in `my-django-app` 

## Requirements
Check instructions in [SETUP-ENV-Kubernetes.md](../../../SETUP-ENV-Kubernetes.md)

## Build & Deploy
Check the Makefile to see the details of the commands.

### Deploy the Datadog operator

- Update the agent helm charts and deploy the operator
```make agent-install DATADOG_API_KEY=<your_api_key>```

#### Optional
- Upgrade the operator values
```make agent-upgrade```

- Delete the operator and agents 
```make agent-delete```

### Deploy the Django boilerplate application

- Build the Django image
```make django-build```

- Deploy the Django app
```make django-deploy```

#### Optional
- Delete the application deployment and service
```make django-delete```

## Get Some Traces

Using the `make django-connect`, you should have a window open in your browser.
Navigate the application to generate traces.

![Alt text](/apm/kubernetes/python/django-admission-controller/screenshots/minikube_service.png?raw=true "Minikube Service")

![Alt text](/apm/kubernetes/python/django-admission-controller/screenshots/application.png?raw=true "Django Application")

![Alt text](/apm/kubernetes/python/django-admission-controller/screenshots/traces.png?raw=true "Traces")
