from pathlib import Path
import requests
import sys

def register_schemas():
    registry_url = "http://localhost:8081"
    schemas_path = Path(__file__).parent
    
    print(f"Looking for schemas in {schemas_path}...")
    
    for avsc_file in schemas_path.glob("*.avsc"):
        subject = avsc_file.stem
        schema_text = avsc_file.read_text(encoding="utf-8")
        
        print(f"Registering schema for subject '{subject}'...")
        try:
            response = requests.post(
                f"{registry_url}/subjects/{subject}/versions",
                json={"schema": schema_text},
                timeout=10
            )
            response.raise_for_status()
            print(f"Successfully registered '{subject}'. Version: {response.json()['id']}")
        except Exception as e:
            print(f"Error registering '{subject}': {e}")

if __name__ == "__main__":
    register_schemas()
