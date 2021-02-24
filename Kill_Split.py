import requests
from termcolor import colored
from decouple import config
from Create_Split import selection_environment, selection_workspace


def selection_kill_split():
    split_name = input("Enter the name of the Split you wish to kill: ")
    environment_name = selection_environment()
    workspace_id = selection_workspace()['id']
    kill_split_in_environment(
        workspace_id, environment_name, split_name)


def kill_split_in_environment(workspace_id, environment_name, split_name):
    kill_split_response = requests.post(
        f"https://api.split.io/internal/api/v2/splits/ws/{workspace_id}/{split_name}/environments/{environment_name}/kill", headers={
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + config('ADMIN_API_KEY')
        })
    kill_split_response.status_code
    kill_split_response.json()
    if kill_split_response.status_code != 200:
        print(kill_split_response.json())
    else:
        print(colored(f"You killed {split_name}. RIP.", "red"))
