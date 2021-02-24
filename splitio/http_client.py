import requests
import json

from accounts.user import get_user

base_url = "https://api.split.io/internal/api/v2"

def get(path):
    response = requests.get(f"{base_url}/{path}", headers=headers())
    return handle_response(response)

def post(path, content):
    print(json.dumps(content))
    response = requests.post(f"{base_url}/{path}", headers=headers(), data=content)
    return handle_response(response)

def headers():
    user = get_user()
    if user == None or user.adminapi == None:
        raise RuntimeError("No active admin api key is available")
    admin_api_key = user.adminapi
    return {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + admin_api_key
    }

def handle_response(response):
    if response.status_code != 200:
        url = response.url
        status_code = str(response.status_code)
        result = str(response.json())
        raise RuntimeError(f"Error with request: url={url} code={status_code} result={result}")
    return response.json()