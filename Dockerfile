FROM python:3.8-slim

RUN apt-get update && apt-get install -y unixodbc-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]