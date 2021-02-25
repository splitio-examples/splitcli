from termcolor import colored
from pick import pick
import json

from splitio import splits_api, definitions_api, environments_api
from templates import split_templates
from selectors import core_selectors

def manage_splits():
    workspace = core_selectors.selection_workspace()
    
    while True:
        splits = splits_api.list_splits(workspace["id"])

        title = "Workspace: " + workspace["name"] + "\n"
        if len(splits) == 0:
            title += "No Splits exist yet!"
        else:
            title += "Select Split to Manage"
        
        options = []
        for split in splits:
            option = split
            option["option_name"] = split["name"]
            option["operation"] = lambda: manage_split(workspace, split)
            options.append(option)
        options.append({ "option_name": "Create a new Split", "operation": lambda: create_split(workspace) })
        options.append({ "option_name": "Go back", "go_back": True })
        
        _, go_back = select(title, options)
        if go_back:
            return

def create_split(workspace):
    try:
        split_name = input("Enter a name for your Split: ")
        split_description = input("Enter a description for your Split: ")
        traffic_type = core_selectors.selection_traffic_type(workspace["id"])

        splits_api.create_split(workspace["id"], traffic_type["name"], split_name, split_description)
        output_message("Your Split has been created!")
    except Exception as exc:
        output_message("Could not create Split\n" + str(exc))

def manage_split(workspace, split):
    while True:
        environments = environments_api.list_environments(workspace["id"])

        options = []
        for environment in environments:
            definition = get_definition(workspace, split, environment)
            option = environment
            if definition == None:
                option["option_name"] = "Create in " + option["name"]
            else:
                option["option_name"] = "Manage in " + option["name"]
            option["operation"] = lambda: manage_definition(workspace, split, option)
            option["definition"] = definition
            options.append(option)
        options.append({ "option_name": "Delete Split", "operation": lambda: delete_split(workspace, split), "go_back": True })
        options.append({ "option_name": "Go back", "go_back": True })
        title = "How can we help you with " + split["name"]

        _, go_back = select(title, options)
        if go_back:
            return

def delete_split(workspace, split):
    title = "Are you sure?"
    options = [
        { "option_name": "Yes", "operation": lambda: splits_api.delete_split(workspace["id"], split["name"]) },
        { "option_name": "No", "go_back": True }
    ]
    select(title, options)

def manage_definition(workspace, split, environment):
    while True:
        definition = get_definition(workspace, split, environment)
        title = "Managing " + split["name"] + " in " + environment["name"]

        options = []
        if definition == None:
            options.append({ "option_name": "Create", "operation": lambda: create_definition(workspace, split, environment) })
            options.append({ "option_name": "Go back", "go_back": True })
        else:
            title += "\nDefinition: " + json.dumps(definition)
            options.append({ "option_name": "Update", "operation": option_unavailable })
            if definition.get("killed", False):
                options.append({ "option_name": "Restore", "operation": lambda: restore_definition(workspace, split, environment) })
            else:
                options.append({ "option_name": "Kill", "operation": lambda: kill_definition(workspace, split, environment) })
            options.append({ "option_name": "Delete definition", "operation": lambda: delete_definition(workspace, split, environment) })
            options.append({ "option_name": "Go back", "go_back": True })
    
        _, go_back = select(title, options)
        if go_back:
            return

def get_definition(workspace, split, environment):
    try:
        return definitions_api.get(workspace["id"], environment["name"], split["name"])
    except Exception as _:
        return None

def delete_definition(workspace, split, environment):
    title = "Are you sure?"
    options = [
        { "option_name": "Yes", "operation": lambda: definitions_api.delete(workspace["id"], environment["name"], split["name"]) },
        { "option_name": "No", "go_back": True }
    ]
    select(title, options)

def select_rollout():
    title = "Select the type of rollout"
    options = [
        { "option_name": "Toggled Rollout", "operation": lambda: split_templates.toggleSplit("Create via Split CLI") },
        { "option_name": "Ramped Rollout", "operation": option_unavailable }
    ]
    selection,_ = select(title, options)
    return selection

def create_definition(workspace, split, environment):
    try:
        split_data = select_rollout()
        definitions_api.create(workspace["id"], environment["name"], split["name"], split_data)
        output_message("Your definition has been created!")
    except Exception as exc:
        output_message("Could not create Split\n" + str(exc))

def kill_definition(workspace, split, environment):
    try:
        definitions_api.kill(workspace["id"], environment["name"], split["name"])
        output_message(f"You killed " + split["name"] + " in " + environment["name"] + ". RIP.")
    except Exception as exc:
        output_message("Could not kill Split\n" + str(exc))

def restore_definition(workspace, split, environment):
    try:
        definitions_api.restore(workspace["id"], environment["name"], split["name"])
        output_message(f"You restored " + split["name"] + " in " + environment["name"] + ". It's Alive!!")
    except Exception as exc:
        output_message("Could not restore Split\n" + str(exc))

def promote_definition(workspace, split, environment):
    # split_name = input("Enter the name of the Split you wish to promote: ")
    pass

def option_unavailable():
    output_message("Option unavailable", "Back")

# TODO: Replace pick with something that integrates more seamlessly with users entering data

def output_message(message, option="Continue"):
    pick([option], message)

def select(title, options):
    selection,_ = pick(options, title, options_map_func=lambda x: x["option_name"])
    result = selection["operation"]() if "operation" in selection else None
    return (result, selection.get("go_back", False))