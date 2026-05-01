#!/bin/sh
#
# Container entrypoint.
#
# Toggles between three instrumentation modes via the INSTRUMENT_MODE env var:
#   ssi   (default) - wraps gunicorn with `ddtrace-run` so ddtrace is loaded
#                     BEFORE gunicorn imports the gevent worker class. This
#                     mimics the production K8s Single-Step Instrumentation
#                     ordering (LD_PRELOAD via dd-lib-python-init:4 +
#                     apm-inject:0). This is the ordering suspected of
#                     causing the silent worker hang.
#   auto            - plain gunicorn; ddtrace is loaded via `import ddtrace.auto`
#                     inside wsgi.py, AFTER the gevent worker has called
#                     gevent.monkey.patch_all(). This is the ordering Datadog
#                     recommends for gevent users and should NOT hang.
#   off             - plain gunicorn with DD_TRACE_ENABLED=false. A control
#                     that confirms the app itself works without ddtrace.

set -eu

cd /app/telco_integration

GUNICORN_ARGS="--env DJANGO_SETTINGS_MODULE=${SETTINGS_PATH} telco_integration.wsgi --user www-data --bind 0.0.0.0:8010 --name TelcoGW --workers 9 --timeout 30 --worker-class=gevent --worker-connections=1000"

case "${INSTRUMENT_MODE:-ssi}" in
    ssi)
        echo "[entrypoint] INSTRUMENT_MODE=ssi -> ddtrace-run gunicorn ..."
        echo "[entrypoint]   (mimics K8s SSI: ddtrace loaded BEFORE gevent monkey-patch)"
        exec ddtrace-run gunicorn ${GUNICORN_ARGS}
        ;;
    auto)
        echo "[entrypoint] INSTRUMENT_MODE=auto -> gunicorn ..."
        echo "[entrypoint]   (ddtrace loaded via wsgi.py AFTER gevent monkey-patch: recommended ordering)"
        exec gunicorn ${GUNICORN_ARGS}
        ;;
    off)
        echo "[entrypoint] INSTRUMENT_MODE=off -> gunicorn ... with DD_TRACE_ENABLED=false"
        export DD_TRACE_ENABLED=false
        exec gunicorn ${GUNICORN_ARGS}
        ;;
    *)
        echo "[entrypoint] Unknown INSTRUMENT_MODE='${INSTRUMENT_MODE}' (use: ssi, auto, off)" >&2
        exit 1
        ;;
esac
