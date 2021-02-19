import requests
from pick import pick
from termcolor import colored
from decouple import config


def createSplit():
    split_name = input("Enter a name for your Split: ")
    split_description = input("Enter a description for your Split: ")

    workspace_response = requests.get(
        "https://api.split.io/internal/api/v2/workspaces", headers={
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + config('ADMIN_API_KEY')
        }
    )

    workspace_response.status_code
    workspace_response_data = workspace_response.json()

    if workspace_response != 200:
        # giving me a keyerror here
        workspaceid = workspace_response_data['id']
        print(workspaceid)
        print("-------")
    else:
        print("something")
        #print(f"obtained workspace id: {workspaceid}")

    create_split_response = requests.post(
        f"https://api.split.io/internal/api/v2/splits/ws/{workspaceid}/trafficTypes/user", headers={
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
        print(colored("Your Split has been created!"), "green")
