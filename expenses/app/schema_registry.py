import os
import requests
import json

class SchemaRegistryClient:
    def __init__(self):
        self.url = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")

    def get_schema_by_id(self, schema_id: int):
        """Получает схему по её ID"""
        try:
            response = requests.get(f"{self.url}/schemas/ids/{schema_id}")
            response.raise_for_status()
            return response.json()["schema"]
        except Exception as e:
            print(f"Schema Registry error: {e}")
            return None

schema_client = SchemaRegistryClient()
