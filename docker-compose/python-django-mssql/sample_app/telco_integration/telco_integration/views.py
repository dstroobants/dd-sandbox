import logging
import time

import requests
from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def hello(request):
    logger.info("hello endpoint hit")
    return JsonResponse({"message": "Hello from TelcoGW"})


def health(request):
    return JsonResponse({"status": "ok"})


def db_check(request):
    """Round-trips through pyodbc -> mssql-django -> MSSQL to exercise the
    same DB stack used in production."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
    return JsonResponse({"db": row[0]})


def sleep_view(request, seconds: int):
    """Useful for proving cooperative gevent scheduling: a few concurrent
    requests to /sleep/5 should all return in ~5s, not 5*N seconds."""
    seconds = max(0, min(seconds, 60))
    time.sleep(seconds)
    return JsonResponse({"slept": seconds})


def gateway(request):
    """Realistic gateway-style endpoint: DB lookup + outbound HTTP call.

    Exercises the full stack the application touches per request:
        - pyodbc -> MSSQL (C extension, releases the GIL)
        - requests -> outbound HTTP (gevent-patched socket, ddtrace-instrumented)
        - JSON response
    With both ddtrace and OpenCensus middleware live, every request creates
    spans in two trace systems whose exporter threads compete for locks
    under the gevent loop.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()

    try:
        r = requests.get("http://datadog-agent:8126/info", timeout=3)
        agent_status = r.status_code
    except Exception as exc:  # noqa: BLE001
        agent_status = f"error: {exc}"

    return JsonResponse({
        "db": "ok",
        "agent_info_status": agent_status,
    })
