FROM python:3.8-slim

# Atualize o índice de pacotes
RUN apt-get update && apt-get install -y --no-install-recommends unixodbc-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]