import requests
import json
import logging
import http.client as internal_http_client

from accounts.user import get_user

base_url = "https://api.split.io/internal/api/v2"


def get(path):
    response = requests.get(f"{base_url}/{path}", headers=headers())
    return handle_response(response)

def delete(path):
    response = requests.delete(f"{base_url}/{path}", headers=headers())
    handle_response(response)

def post(path, content=None):
    response = requests.post(f"{base_url}/{path}", headers=headers(), json=content)
    return handle_response(response, content)

def put(path, content=None):
    response = requests.put(f"{base_url}/{path}", headers=headers(), json=content)
    return handle_response(response, content)

def put_file(path, file_path):
    with open(file_path, 'rb') as f:
        response = requests.put(f"{base_url}/{path}", headers=headers(), files={file_path: f})
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

def handle_response(response, payload=None):
    if response.status_code != 200:
        url = response.url
        status_code = str(response.status_code)
        result = str(response.json())
        raise RuntimeError(f"Error with request: url={url} payload={payload} code={status_code} result={result}")
    return response.json()