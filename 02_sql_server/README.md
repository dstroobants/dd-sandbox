# dd-sandbox

## Get Started

1. Input your Datadog API Key in `Dockerfile.datadog-agent`
2. Build with `make build`
3. `docker-compose up` to run and `docker-compose down` to stop
4. Optional: To delete the DB and start fresh, run `docker-compose down` a second time

## Reasons why SQL Server on Linux sucks and why this sandbox exists

https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server

Your first instinct would be to try to install the odbc drivers on a Datadog Agent container so
you can connect to your SQL Server Database and monitor it.

The problem is that this impossible, the Datadog Agent images are based on Ubuntu and installations
results in this error message: Ubuntu <release_name> is not currently supported."

Therefore you need to install the agent on a Linux distribution that supports ODBC drivers.
So you try a Debian12, as it says that this is supported on the Microsoft Documentation:

The reality is that there are no microsoft odbc package for debian12, the documentation is 
incorrect and packages are missing.

Therefore we settled on a Debian 11 image where we install the Datadog Agent Manually.
