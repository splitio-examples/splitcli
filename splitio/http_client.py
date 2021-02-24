import requests

from accounts.user import get_user

base_url = "https://api.split.io/internal/api/v2"

def get(path):
    response = requests.get(f"{base_url}/{path}", headers=headers())
    return handle_response(response)

def post(path, content):
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
        raise RuntimeError("Error posting data: code=" + str(response.status_code) + " error=" + str(response.json()))
    return response.json()