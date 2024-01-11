from google.oauth2 import service_account

CREDENTIALS = service_account.Credentials.from_service_account_file('api/models/llm/credentials.json')

PROJECT = "base-map-workspace"

LOCATION = "us-central1"
