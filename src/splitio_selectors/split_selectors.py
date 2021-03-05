import json

from splitio import splits_api, definitions_api, environments_api
from templates import split_templates
from splitio_selectors import core_selectors
from ux.menu import option_unavailable, success_message, error_message, info_message, select_operation, text_input, error_message, select_strings

def manage_splits():
    workspace = core_selectors.selection_workspace()

    while True:
        splits = splits_api.list_splits(workspace["id"])

        print("Workspace: " + workspace["name"])
        title = ""
        if len(splits) == 0:
            title += "No splits exist yet"
        else:
            title += "Select split to Manage"

        options = []
        for split in splits:
            option = split
            option["option_name"] = split["name"]
            option["operation"] = lambda bound_split=split: manage_split(workspace, bound_split)
            options.append(option)
        options.append({"option_name": "Create a new split", "operation": lambda: create_split(workspace)})
        options.append({"option_name": "Go back", "go_back": True})

        _, go_back = select_operation(title, options)
        if go_back:
            return

def create_split(workspace):
    try:
        split_name = text_input("Enter a name for your split: ")
        split_description = text_input("Enter a description for your split: ")
        traffic_type = core_selectors.selection_traffic_type(workspace["id"])

        (treatments, baseline) = select_treatments()

        splits_api.create_split(workspace["id"], traffic_type["name"], split_name, split_description)

        create_split_in_all_environments(workspace, split_name, treatments, baseline)
        success_message("Your split has been created!")
    except Exception as exc:
        error_message("Could not create split\n" + str(exc))

def create_split_in_all_environments(workspace, split_name, treatments, baseline):
    environments = environments_api.list_environments(workspace["id"])
    for environment in environments:
        create_definition(workspace, split_name, environment)

def select_treatments():
    title = "Select Treatments"
    options = [
        {"option_name": "Toggle (on/off)", "operation": lambda: (["on", "off"], "off")},
        {"option_name": "Custom", "operation": lambda: input_treatments()}
    ]
    selection,_ = select_operation(title, options)
    return selection

def input_treatments():
    treatments = []
    while True:
        treatment = text_input("Add treatment name (empty when done)")
        if treatment == "":
            if len(treatments) < 2:
                error_message("At least two treatments are required")
            else:
                break
        else:
            treatments.append(treatment)
    baseline,_ = select_strings("Select baseline treatment", treatments)
    return (treatments, baseline)

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
            option["operation"] = lambda bound_option=option: manage_definition(workspace, split, bound_option)
            options.append(option)
        options.append({"option_name": "Delete split", "operation": lambda: delete_split(workspace, split), "go_back": True})
        options.append({"option_name": "Go back", "go_back": True})
        title = "Managing split: " + split["name"]

        _, go_back = select_operation(title, options)
        if go_back:
            return


def delete_split(workspace, split):
    title = "Are you sure?"
    options = [
        {"option_name": "Yes", "operation": lambda: splits_api.delete_split(
            workspace["id"], split["name"])},
        {"option_name": "No", "go_back": True}
    ]
    select_operation(title, options)

def manage_definition(workspace, split, environment):
    while True:
        definition = get_definition(workspace, split, environment)
        if definition == None:
            (treatments, baseline) = select_treatments()
            create_definition(workspace, split["name"], environment, treatments, baseline)
        else:
            title = "Managing " + split["name"] + " in " + environment["name"]

            options = []
            options.append({"option_name": "Show definition", "operation": lambda: show_definition(definition)})
            options.append({"option_name": "Update", "operation": option_unavailable})
            if definition.get("killed", False):
                options.append({"option_name": "Restore", "operation": lambda: restore_definition(workspace, split, environment)})
            else:
                options.append({"option_name": "Kill", "operation": lambda: kill_definition(workspace, split, environment)})
            options.append({"option_name": "Delete definition", "go_back": True, "operation": lambda: delete_definition(workspace, split, environment)})
            options.append({"option_name": "Go back", "go_back": True})

            _, go_back = select_operation(title, options)
            if go_back:
                return

def show_definition(definition):
    info_message("Definition: " + json.dumps(definition, indent=4))

def get_definition(workspace, split, environment):
    try:
        return definitions_api.get(workspace["id"], environment["name"], split["name"])
    except Exception as _:
        return None


def delete_definition(workspace, split, environment):
    title = "Are you sure?"
    options = [
        {"option_name": "Yes", "operation": lambda: definitions_api.delete(
            workspace["id"], environment["name"], split["name"])},
        {"option_name": "No", "go_back": True}
    ]
    select_operation(title, options)

def create_definition(workspace, split_name, environment, treatments=["on", "off"], baseline="off"):
    try:
        split_data = split_templates.new_split(treatments, baseline)
        definitions_api.create(workspace["id"], environment["name"], split_name, split_data)
    except Exception as exc:
        error_message("Could not create split\n" + str(exc))

def kill_definition(workspace, split, environment):
    try:
        definitions_api.kill(
            workspace["id"], environment["name"], split["name"])
        success_message(f"You killed " + split["name"] + " in " + environment["name"] + ". RIP.")
    except Exception as exc:
        error_message("Could not kill split\n" + str(exc))

def restore_definition(workspace, split, environment):
    try:
        definitions_api.restore(
            workspace["id"], environment["name"], split["name"])
        success_message(f"You restored " + split["name"] + " in " + environment["name"] + ". It's Alive!!")
    except Exception as exc:
        error_message("Could not restore split\n" + str(exc))