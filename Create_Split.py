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


def toggleSplit(comment):
    return rampSplit(0, comment)


def rampSplit(ramp, comment):
    return {
        "treatments": [
            {
                "name": "on"
            },
            {
                "name": "off"
            }
        ],
        "defaultTreatment": "off",
        "baselineTreatment": "off",
        "rules": [],
        "defaultRule": [
            {
                "treatment": "on",
                "size": ramp
            },
            {
                "treatment": "off",
                "size": 100 - ramp
            }
        ],
        "comment": comment
    }


def createSplit():
    split_name = input("Enter a name for your Split: ")

    print("Select the type of Split")
    print("1. Toggle Split")
    selection = input("Selection: ")
    if selection == "1":

        workspace = get_workspace('Default')
        if workspace == None:
            print("ERROR")
            return
        workspace_id = workspace['id']

        environment_name = "Prod-Default"

        split_data = toggleSplit("Create via Split CLI")

        create_split_response = requests.post(
            f"https://api.split.io/internal/api/v2/splits/ws/{workspace_id}/{split_name}/environments/{environment_name}", headers={
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + config('ADMIN_API_KEY')
            }, data=split_data)

    create_split_response.status_code
    create_split_response.json()

    if create_split_response.status_code != 200:
        print(create_split_response.json())
    else:
        print(colored("Your Split has been created!", "green"))
