import requests
import time

from splitcli.accounts.user import get_user
from splitcli.ux import menu

max_retries = 3
base_url = "https://api.split.io/internal/api/v2"


def get(path):
    return execute_request(lambda: requests.get(f"{base_url}/{path}", headers=headers()))

def delete(path):
    execute_request(lambda: requests.delete(f"{base_url}/{path}", headers=headers()))

def post(path, content=None):
    return execute_request(lambda: requests.post(f"{base_url}/{path}", headers=headers(), json=content))

def put(path, content=None):
    return execute_request(lambda: requests.put(f"{base_url}/{path}", headers=headers(), json=content))

def put_file(path, file_path):
    with open(file_path, 'rb') as f:
        return execute_request(lambda: requests.put(f"{base_url}/{path}", headers=headers(), files={file_path: f}))

# Helper Functions

def execute_request(operation):
    retries = 0
    while retries < max_retries:
        (success, response) = handle_response(operation())
        if success:
            return response
        retries += 1

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
    if response.status_code == 429:
        # Add a sleep
        menu.warn_message("Requests are rate limited (max 30 per 10s). Waiting...")
        time.sleep(10)
        return (False, None)
    if response.status_code != 200:
        url = response.url
        status_code = str(response.status_code)
        result = str(response.json())
        raise RuntimeError(f"Error with request: url={url} code={status_code} result={result}")
    return (True, response.json())