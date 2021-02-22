import requests
from pick import pick
from termcolor import colored
from decouple import config


def list_workspaces():
    workspaces_url = 'https://api.split.io/internal/api/v2/workspaces'
    response = requests.get(workspaces_url, headers={
                            "Authorization": "Bearer " + config('ADMIN_API_KEY')})
    if response.status_code == 200:
        return response.json()['objects']
    else:
        return []


def get_workspace(name):
    workspaces = list_workspaces()
    workspaces = list(filter(lambda x: x['name'] == name, workspaces))
    if len(workspaces) == 0:
        return None
    else:
        return workspaces[0]


def createSplit():
    split_name = input("Enter a name for your Split: ")
    split_description = input("Enter a description for your Split: ")

    workspace = get_workspace('Default')
    if workspace == None:
        print("ERROR")
        return
    workspace_id = workspace['id']

    traffic_type_name = 'user'

    create_split_response = requests.post(
        f"https://api.split.io/internal/api/v2/splits/ws/{workspace_id}/trafficTypes/{traffic_type_name}", headers={
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + config('ADMIN_API_KEY')
        }, json={
            "name":  split_name,
            "description": split_description
        })

    create_split_response.status_code
    create_split_response.json()

    if create_split_response.status_code != 200:
        print(create_split_response.json())
    else:
        print(colored("Your Split has been created!", "green"))
