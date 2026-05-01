"""
WSGI config for telco_integration project.

It exposes the WSGI callable as a module-level variable named ``application``.

Note on instrumentation:
    In production the application runs under Kubernetes Single-Step
    Instrumentation (LD_PRELOAD via dd-lib-python-init:4 + apm-inject:0),
    which loads ddtrace BEFORE the Python interpreter executes any user
    code. To replicate that ordering in docker-compose without pulling the
    SSI init images, the entrypoint wraps gunicorn with `ddtrace-run`. By
    the time wsgi.py is imported (post-fork, post-gevent-monkeypatch)
    ddtrace is already loaded.

    `import ddtrace.auto` here is therefore a no-op in the SSI-mimic path,
    but is left in place so that toggling `ddtrace-run` off in the entrypoint
    still instruments the app the way Datadog recommends for gevent users
    (i.e. AFTER monkey-patching).
"""

import os

import ddtrace.auto  # noqa: F401  (see module docstring)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telco_integration.settings")

application = get_wsgi_application()
