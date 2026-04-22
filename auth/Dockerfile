FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl gcc libc6-dev libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn "uvicorn[standard]"

COPY app/ .

CMD ["gunicorn", "main:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
"

COPY app/*.py ./

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "1", "main:app"]