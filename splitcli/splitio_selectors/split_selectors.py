from splitcli.split_apis import splits_api, environments_api
from splitcli.splitio_selectors import core_selectors, definition_selectors
from splitcli.ux import menu

def manage_splits():
    workspace = core_selectors.selection_workspace()

    while True:
        splits = splits_api.list_splits(workspace["id"])
        title = None
        if len(splits) == 0:
            title = "No splits exist yet"
        else:
            title = "Select split to Manage"

        options = []
        for split in splits:
            option = split
            option["option_name"] = split["name"]
            option["operation"] = lambda bound_split=split: manage_split(workspace, bound_split)
            options.append(option)
        options.append({"option_name": "Create a new split", "operation": lambda: create_split(workspace)})
        options.append({"option_name": "Go back", "go_back": True})

        _, go_back = menu.select_operation(title, options)
        if go_back:
            return

def create_split(workspace):
    try:
        split_name = menu.text_input("Enter a name for your split")
        split_description = menu.text_input("Enter a description for your split")
        traffic_type = core_selectors.selection_traffic_type(workspace["id"])

        (treatments, baseline) = definition_selectors.select_treatments()

        create_split_operator(workspace["id"], traffic_type["name"], split_name, split_description, treatments, baseline)
        menu.success_message("Your split has been created!")

        split = splits_api.get_split(workspace['id'], split_name)
        manage_split(workspace, split)
    except Exception as exc:
        menu.error_message("Could not create split\n" + str(exc))

def manage_split(workspace, split):
    while True:
        environments = environments_api.list_environments(workspace["id"])

        options = []
        for environment in environments:
            definition = definition_selectors.get_definition_operator(workspace, split, environment)
            option = environment
            if definition == None:
                option["option_name"] = "Create in " + option["name"]
            else:
                option["option_name"] = "Manage in " + option["name"]
            option["operation"] = lambda bound_option=option: definition_selectors.manage_definition(workspace, split, bound_option)
            options.append(option)
        options.append({"option_name": "Delete split", "operation": lambda: delete_split(workspace, split), "go_back": True})
        options.append({"option_name": "Go back", "go_back": True})
        title = "Managing split: " + split["name"]

        _, go_back = menu.select_operation(title, options)
        if go_back:
            return

def delete_split(workspace, split):
    title = "Are you sure?"
    options = [
        {"option_name": "Yes", "operation": lambda: splits_api.delete_split(workspace["id"], split["name"])},
        {"option_name": "No", "go_back": True}
    ]
    menu.select_operation(title, options)

# Operators

def create_split_operator(workspace_id, traffic_type_name, split_name, split_description="", treatments=["on","off"], baseline="off"):
    # Create Metadata
    splits_api.create_split(workspace_id, traffic_type_name, split_name, split_description)

    # Create in all environments
    environments = environments_api.list_environments(workspace_id)
    for environment in environments:
        definition_selectors.create_definition_operator(workspace_id, environment["name"], split_name, treatments, baseline)