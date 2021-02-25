from termcolor import colored
from pick import pick

from splitio import splits_api
from splitio import definitions_api
from templates import split_templates
from selectors import core_selectors

def select_split(workspace_id):
    splits = splits_api.list_splits(workspace_id)
    title = "Select Split to Manage"
    split = pick(splits, title, )


def selection_split_type():
    print("Select the type of Split")
    print("1. Toggle Split")
    selection = input("Selection: ")
    if selection == "1":
        return split_templates.toggleSplit("Create via Split CLI")

def selection_get_split():
    environment_name = core_selectors.selection_environment()
    workspace_id = core_selectors.selection_workspace()['id']
    split_name = input("Enter a name for your Split: ")
    return definitions_api.get_split_definition(workspace_id, split_name, environment_name)

def selection_create_split():
    try:
        split_name = input("Enter a name for your Split: ")
        split_description = input("Enter a description for your Split: ")

        traffic_type_name = core_selectors.selection_traffic_type()
        environment_name = core_selectors.selection_environment()
        workspace_id = core_selectors.selection_workspace()['id']
        
        split_data = selection_split_type()

        splits_api.create_split(workspace_id, traffic_type_name,
                     split_name, split_description)
        definitions_api.create_split_in_environment(
            workspace_id, environment_name, split_name, split_data)
        print(colored("Your Split has been created!", "green"))
    except Exception as exc:
        print("Could not create Split")
        print(exc)

def selection_kill_split():
    try:
        split_name = input("Enter the name of the Split you wish to kill: ")

        environment_name = core_selectors.selection_environment()
        workspace_id = core_selectors.selection_workspace()['id']

        definitions_api.kill_split_in_environment(
            workspace_id, environment_name, split_name)
        print(colored(f"You killed {split_name}. RIP.", "red"))
    except Exception as exc:
        print("Could not kill Split")
        print(exc)