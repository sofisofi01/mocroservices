FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY connectors/ connectors/

ENTRYPOINT ["python", "main.py"]
