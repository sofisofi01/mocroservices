import requests
import json
import time
import sys
from pathlib import Path

def register_connectors():

    connectors_dir = Path("connectors")
    if not connectors_dir.exists():
        print(f"Error: {connectors_dir} not found")
        sys.exit(1)

    print(f"Waiting for Debezium Connect to be ready...")
    for i in range(30):
        try:
            r = requests.get("http://connect:8083/connectors", timeout=5)
            if r.status_code == 200:
                print("Connect is ready!")
                break
        except Exception:
            pass
        time.sleep(2)
    else:
        print("Error: Debezium Connect is not reachable")
        sys.exit(1)

    for config_path in connectors_dir.glob("*.json"):
        data = json.loads(config_path.read_text(encoding="utf-8"))
        name = data['name']
        config = data['config']
        url = f"http://connect:8083/connectors/{name}"

        print(f"Checking if connector '{name}' exists...")
        r = requests.get(f"{url}/config", timeout=5)
        
        if r.status_code == 200:
            print(f"Connector '{name}' exists. Updating configuration...")
            requests.put(f"{url}/config", json=config, timeout=30).raise_for_status()
            print(f"Update for '{name}' successful.")
        else:
            print(f"Connector '{name}' not found. Creating new one...")
            requests.post("http://connect:8083/connectors", json=data, timeout=30).raise_for_status()
            print(f"Creation of '{name}' successful.")

def register_schemas():
    schemas_dir = Path("schemas")
    if not schemas_dir.exists():
        print(f"No schemas directory found, skipping.")
        return

    print("Waiting for Schema Registry to be ready...")
    for i in range(30):
        try:
            r = requests.get("http://schema-registry:8081/subjects", timeout=5)
            if r.status_code == 200:
                print("Schema Registry is ready!")
                break
        except Exception:
            pass
        time.sleep(2)
    else:
        print("Error: Schema Registry is not reachable")
        return

    for schema_path in schemas_dir.glob("*.avsc"):
        subject = schema_path.stem
        schema_content = schema_path.read_text(encoding="utf-8")
        
        print(f"Registering schema for subject '{subject}'...")
        payload = {"schema": schema_content}
        r = requests.post(
            f"http://schema-registry:8081/subjects/{subject}/versions",
            json=payload,
            timeout=10
        )
        if r.status_code == 200:
            print(f"Schema '{subject}' registered successfully.")
        else:
            print(f"Failed to register schema '{subject}': {r.text}")

if __name__ == "__main__":
    register_connectors()
