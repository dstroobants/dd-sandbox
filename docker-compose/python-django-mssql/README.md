# Django + gunicorn (gevent) workers

## Production deployment shape

The original application is deployed in Kubernetes with Datadog
**Single-Step Instrumentation** (SSI):

- Init containers `dd-lib-python-init:4` + `apm-inject:0` install dd-trace-py
  4.x and wire `LD_PRELOAD=/opt/datadog-packages/datadog-apm-inject/stable/inject/launcher.preload.so`.
- The application is launched with:

  ```
  (cd telco_integration; \
     gunicorn --env DJANGO_SETTINGS_MODULE=$SETTINGS_PATH telco_integration.wsgi \
              --user www-data --bind 0.0.0.0:8010 --name TelcoGW \
              --workers 9 --timeout 30 \
              --worker-class=gevent --worker-connections=1000)
  ```

`LD_PRELOAD` causes `ddtrace` to be loaded **before the Python interpreter
runs any user code** — so by the time gunicorn's gevent worker calls
`gevent.monkey.patch_all()` in each forked worker, `ddtrace` has already
created threads, locks, and sockets against the *un-patched* stdlib. That
combination is a known source of silent deadlocks: greenlets call into
`ddtrace`, the tracer's internal writer thread tries to acquire a real
`threading.Lock`, and nothing ever runs the gevent loop again. Workers go
silent (no logs, no errors), the `--timeout 30` reaper eventually kills them,
and gunicorn forks fresh ones that hang the same way.

## What this repo reproduces

A minimal Django 3.2 app named `telco_integration` running under the
production gunicorn command and the *exact* pinned dependency set from the
production environment (see `sample_app/requirements.txt`). The Dockerfile
installs Python 3.10.4 + `msodbcsql18` so `pyodbc` / `mssql-django` resolve
the same way they do in the production image.

`docker-compose.yml` brings up:

| Service        | Image                                | Notes                                            |
| -------------- | ------------------------------------ | ------------------------------------------------ |
| `djangoapp`    | built from `sample_app/Dockerfile`   | runs the production gunicorn command             |
| `mssql`        | `mcr.microsoft.com/mssql/server:2022-latest` | gives `mssql-django` a real DB to connect to    |
| `datadog-agent`| `gcr.io/datadoghq/agent:latest`      | site `datadoghq.eu`, mirrors production tracer config |

## Prerequisites

1. Docker / Docker Compose installed.
2. A `~/sandbox.docker.env` file containing at least:

   ```
   DD_API_KEY=<your dev API key>
   ```

   (referenced by `docker-compose.yml` for the `datadog-agent` service)

## Running

```bash
docker compose build
docker compose up
```

Then in another terminal:

```bash
curl -v --max-time 5 http://localhost:8010/
curl -v --max-time 5 http://localhost:8010/health/
curl -v --max-time 5 http://localhost:8010/db/
curl -v --max-time 5 http://localhost:8010/gateway/
```

## Toggling the instrumentation mode

The image's entrypoint reads `INSTRUMENT_MODE` (set in `docker-compose.yml`)
and switches between three configurations so the ordering hypothesis can be
tested directly:

| `INSTRUMENT_MODE` | Effective command                                    | Purpose                                                                 |
| ----------------- | ---------------------------------------------------- | ----------------------------------------------------------------------- |
| `ssi` *(default)* | `ddtrace-run gunicorn …`                             | mimics K8s SSI ordering — ddtrace loaded *before* gevent monkey-patch   |
| `auto`            | `gunicorn …` + `import ddtrace.auto` inside wsgi.py  | recommended order for gevent users — ddtrace loaded *after* monkey-patch |
| `off`             | `gunicorn …` with `DD_TRACE_ENABLED=false`           | control / no instrumentation                                            |

To switch:

```bash
INSTRUMENT_MODE=auto docker compose up djangoapp        # no rebuild needed
INSTRUMENT_MODE=off  docker compose up djangoapp
```

Or edit the `INSTRUMENT_MODE:` line under `services.djangoapp.environment` in
`docker-compose.yml`.

## Endpoints

| Path                | What it does                                                                      |
| ------------------- | --------------------------------------------------------------------------------- |
| `/`                 | logs + returns `{"message": "Hello from TelcoGW"}`                                |
| `/health/`          | returns `{"status": "ok"}` (no DB, no logging — useful for isolating the hang)     |
| `/db/`              | runs `SELECT 1` over `pyodbc` → MSSQL                                              |
| `/gateway/`         | DB lookup + outbound `requests.get` (exercises the requests integration)           |
| `/sleep/<seconds>/` | `time.sleep(seconds)` — useful for confirming gevent cooperative scheduling       |

## Current status — what reproduces and what doesn't

The scaffold runs `ddtrace-run gunicorn … --worker-class=gevent` against
Django 3.2 with the production-pinned dependency set, the
`OpencensusMiddleware` registered, and pyodbc → MSSQL wired up. Across all
the configurations tried so far, **the application does not hang**:

| Configuration                                                                               | Behaviour                                              |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `GET /health/` single                                                                       | 200 in <100 ms                                         |
| `GET /` single                                                                              | 200 in <100 ms                                         |
| `GET /db/` (pyodbc → MSSQL) single                                                          | 200 in <100 ms                                         |
| `GET /sleep/3/` × 2 parallel                                                                | both 3 s (gevent cooperative scheduling alive)         |
| `ab -t 30 -c 200 /db/`  (~12k reqs)                                                         | 0 failed, p99 ≈ 720 ms                                 |
| `ab -t 30 -c 200 /gateway/` (DB + outbound `requests.get`)                                  | 0 failed, p99 ≈ 779 ms                                 |
| `OpencensusMiddleware` + ddtrace 4.8.0 + gevent 26.4.0 + pyodbc 5.3.0 + requests 2.25.1     | no deadlock under load                                 |

## Layout

```
.
├── README.md
├── docker-compose.yml
└── sample_app/
    ├── Dockerfile
    ├── entrypoint.sh
    ├── requirements.txt
    └── telco_integration/             # outer dir (gunicorn cd's into this)
        ├── manage.py
        └── telco_integration/         # inner Django module
            ├── __init__.py
            ├── settings.py
            ├── settings_uat.py        # SETTINGS_PATH=telco_integration.settings_uat
            ├── urls.py
            ├── views.py
            └── wsgi.py
```
