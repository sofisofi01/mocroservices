import os
import requests
import json

class SchemaRegistryClient:
    def __init__(self):
        self.url = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")

    def register_schema(self, subject: str, schema_dict: dict):
        """Регистрирует схему для указанного субъекта"""
        try:
            response = requests.post(
                f"{self.url}/subjects/{subject}/versions",
                json={"schema": json.dumps(schema_dict)}
            )
            response.raise_for_status()
            return response.json()["id"]
        except Exception as e:
            print(f"Schema Registry error: {e}")
            return None

    def get_latest_schema(self, subject: str):
        """Получает последнюю версию схемы"""
        try:
            response = requests.get(f"{self.url}/subjects/{subject}/versions/latest")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Schema Registry error: {e}")
            return None

schema_client = SchemaRegistryClient()
