FROM python:3.12

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --upgrade pip

# Copy and install custom ddtrace wheel (if it exists)
COPY ddtrace*.whl /tmp/ 2>/dev/null || true
RUN if ls /tmp/ddtrace*.whl 1> /dev/null 2>&1; then \
      pip install --no-cache-dir /tmp/ddtrace*.whl && rm /tmp/ddtrace*.whl; \
    else \
      echo "No custom ddtrace wheel found, installing from requirements.txt"; \
    fi

# Install remaining requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

# Create a startup script that runs migrations and then starts the server
COPY startup.sh ./
RUN chmod +x startup.sh

CMD ["./startup.sh"]
