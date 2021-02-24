from termcolor import colored

from splitio import splits
from templates import split_templates
from selectors import core_selectors


def selection_split_type():
    print("Select the type of Split")
    print("1. Toggle Split")
    selection = input("Selection: ")
    if selection == "1":
        return split_templates.toggleSplit("Create via Split CLI")


def selection_get_split():
    workspace_id = core_selectors.selection_workspace()['id']
    environment_name = core_selectors.selection_environment(workspace_id)
    split_name = input("Enter a name for your Split: ")
    return splits.get_split(workspace_id, split_name, environment_name)


def selection_create_split():
    try:
        split_name = input("Enter a name for your Split: ")
        split_description = input("Enter a description for your Split: ")
        workspace_id = core_selectors.selection_workspace()['id']
        traffic_type = core_selectors.selection_traffic_type(workspace_id)
        environment = core_selectors.selection_environment(workspace_id)

        split_data = selection_split_type()

        splits.create_split(workspace_id, traffic_type["name"],
                            split_name, split_description)
        splits.create_split_in_environment(
            workspace_id, environment["name"], split_name, split_data)
        print(colored("Your Split has been created!", "green"))
    except Exception as exc:
        print("Could not create Split")
        print(exc)


def selection_kill_split():
    try:
        split_name = input("Enter the name of the Split you wish to kill: ")
        workspace_id = core_selectors.selection_workspace()['id']
        environment_name = core_selectors.selection_environment(workspace_id)

        splits.kill_split_in_environment(
            workspace_id, environment_name, split_name)
        print(colored(f"You killed {split_name}. RIP.", "red"))
    except Exception as exc:
        print("Could not kill Split")
        print(exc)


def selection_promote_split():
    split_name = input("Enter the name of the Split you wish to promote: ")
    workspace_id = core_selectors.selection_workspace()['id']
    environment_name = core_selectors.selection_environment(workspace_id)
