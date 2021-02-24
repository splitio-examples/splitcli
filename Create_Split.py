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
        # "baselineTreatment": "off",
        # "rules": [],
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
        # "comment": comment
    }


def movie():
    return {
        "name": "movie_filter",
        # "environment": {
        #     "id": "f8aa2660-3f31-11eb-be37-12b057418355",
        #     "name": "Prod-Default"
        # },
        # "trafficType": {
        #     "id": "f8a8ede0-3f31-11eb-be37-12b057418355",
        #     "name": "user"
        # },
        "killed": False,
        "treatments": [
            {
                "name": "USA",
                "description": "USA Filter"
            },
            {
                "name": "default",
                "description": ""
            }
        ],
        "defaultTreatment": "USA",
        "baselineTreatment": "default",
        "trafficAllocation": 100,
        "rules": [],
        "defaultRule": [
            {
                "treatment": "USA",
                "size": 100
            }
        ],
        # "creationTime": 1613767914941,
        # "lastUpdateTime": 1613768561090
    }


def createSplit():
    split_name = input("Enter a name for your Split: ")

    print("Select the type of Split")
    print(colored("1. Toggle Split", "green"))
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


def create_split(workspace_id, traffic_type_name, split_name, split_description):
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


def create_split_in_environment(workspace_id, environment_name, split_name, split_data):
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


def selection_split_type():
    print("Select the type of Split")
    print("1. Toggle Split")
    selection = input("Selection: ")
    if selection == "1":
        return movie()  # toggleSplit("Create via Split CLI")


def selection_environment():
    # todo: add selection
    return "Staging-Default"


def selection_traffic_type():
    # todo: add selection
    return "user"


def selection_workspace():
    # todo: add selection
    workspace = get_workspace('Default')
    if workspace == None:
        print("ERROR")
        return None
    return workspace


def selection_create_split():
    split_name = input("Enter a name for your Split: ")
    split_description = input("Enter a description for your Split: ")

    traffic_type_name = selection_traffic_type()

    split_data = selection_split_type()
    environment_name = selection_environment()
    workspace_id = selection_workspace()['id']
    create_split(workspace_id, traffic_type_name,
                 split_name, split_description)
    create_split_in_environment(
        workspace_id, environment_name, split_name, split_data)


def selection_get_split():
    environment_name = selection_environment()
    workspace_id = selection_workspace()['id']
    split_name = input("Enter a name for your Split: ")
    get_split(workspace_id, split_name, environment_name)


def get_split(workspace_id, split_name, environment_name):
    fetch_split_response = requests.get(
        f"https://api.split.io/internal/api/v2/splits/ws/{workspace_id}/{split_name}/environments/{environment_name}", headers={
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + config('ADMIN_API_KEY')
        })
    print(fetch_split_response.json())
