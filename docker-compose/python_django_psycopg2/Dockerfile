FROM python:3.12

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

# Create a startup script that runs migrations and then starts the server
COPY startup.sh ./
RUN chmod +x startup.sh

CMD ["./startup.sh"]
