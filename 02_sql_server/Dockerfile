# There is no microsoft odbc package for debian12 so we stick with 11 for now (documentation is wrong and outdated)
FROM python:3-bullseye

WORKDIR /odbc-driver

# Install SQL Server driver
# https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

#Debian 9-11
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc

#Debian 11
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN sed -i 's| signed-by=/usr/share/keyrings/microsoft-prod.gpg||' /etc/apt/sources.list.d/mssql-release.list \
  && cat /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18
ENV PATH="$PATH:/opt/mssql-tools18/bin"
# optional: for unixODBC development headers
# optional: kerberos library for debian-slim distributions
RUN apt-get install -y unixodbc-dev libgssapi-krb5-2

WORKDIR /usr/src/app

# Install Script APP

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y unixodbc-dev

COPY app/. .

CMD [ "python", "-u", "script.py" ]
