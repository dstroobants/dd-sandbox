# syntax=docker/dockerfile:1
#
# Django + gunicorn + gevent + Datadog reproduction.
#
# Python is pinned to 3.10.4 to match the production runtime exactly.

ARG PYTHON_VERSION=3.10.4
FROM python:${PYTHON_VERSION}-slim-bullseye AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Build / runtime libraries needed by:
#   - pyodbc 5.3.0           -> unixodbc-dev
#   - cryptography 47.0.0    -> libssl-dev (only if no wheel; usually wheel exists)
#   - cffi 2.0.0 / lxml 6.x  -> build-essential, libffi-dev, libxml2-dev, libxslt1-dev
#   - gevent / greenlet      -> build-essential (only if no wheel)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        gnupg \
        libffi-dev \
        libssl-dev \
        libxml2-dev \
        libxslt1-dev \
        unixodbc-dev \
 && rm -rf /var/lib/apt/lists/*

# Microsoft ODBC Driver 18 for SQL Server (Debian 11 / Bullseye).
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
        | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
 && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" \
        > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
 && rm -rf /var/lib/apt/lists/*

# 1) Install the production-pinned dependency set first so the resolver
#    doesn't bump anything, exactly the way it lands in the production
#    container. NOTE: pip is intentionally NOT upgraded. Python 3.10.4 ships
#    with pip 22.0.4, which is lenient about old PEP 440 metadata
#    (e.g. celery==5.0.5 has `pytz (>dev)` markers that pip>=24.1 rejects).
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2) Overlay ddtrace 4.x on top, just like the K8s init container
#    (dd-lib-python-init:4) does at pod start. Using a separate layer means
#    ddtrace can pull whatever transitive deps it needs without conflicting
#    with the resolver run above.
RUN pip install 'ddtrace>=4.7,<5'

# Application source. The production gunicorn command is
# `cd telco_integration; gunicorn telco_integration.wsgi ...`, so the project
# lives at /app/telco_integration/ with the inner Django module at
# /app/telco_integration/telco_integration/.
COPY telco_integration ./telco_integration

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8010

# www-data exists in debian-slim by default; gunicorn drops to it via --user,
# so the container itself starts as root.

ENTRYPOINT ["/entrypoint.sh"]
