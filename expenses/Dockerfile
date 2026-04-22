FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl gcc libc6-dev librdkafka-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir "confluent-kafka[schemaregistry]"
RUN pip install --no-cache-dir gunicorn "uvicorn[standard]"

COPY app/ .

CMD ["gunicorn", "main:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
