import requests
import json
import logging
import http.client as internal_http_client

from accounts.user import get_user

base_url = "https://api.split.io/internal/api/v2"

# enable_debug()

def get(path):
    response = requests.get(f"{base_url}/{path}", headers=headers())
    return handle_response(response)

def delete(path):
    response = requests.delete(f"{base_url}/{path}", headers=headers())
    handle_response(response)

def post(path, content):
    response = requests.post(f"{base_url}/{path}", headers=headers(), json=content)
    return handle_response(response)

def put(path, content):
    response = requests.put(f"{base_url}/{path}", headers=headers(), json=content)
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

def enable_debug():
    internal_http_client.HTTPConnection.debuglevel = 1
    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True