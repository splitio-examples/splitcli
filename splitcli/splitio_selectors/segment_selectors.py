from splitcli.split_apis import segments_api, environments_api
from splitcli.splitio_selectors import core_selectors
from splitcli.ux import menu

def manage_segments():
    workspace = core_selectors.selection_workspace()

    while True:
        segments = segments_api.list_segments(workspace["id"])
        title = None
        if len(segments) == 0:
            title = "No segments exist yet"
        else:
            title = "Select segment to Manage"

        options = []
        for segment in segments:
            option = segment
            option["option_name"] = segment["name"]
            option["operation"] = lambda bound_segment=segment: manage_segment(workspace, bound_segment["name"])
            options.append(option)
        options.append({"option_name": "Create a new segment", "operation": lambda: create_segment(workspace)})
        options.append({"option_name": "Go back", "go_back": True})

        _, go_back = menu.select_operation(title, options)
        if go_back:
            return

def create_segment(workspace):
    try:
        segment_name = menu.text_input("Enter a name for your segment")
        segment_description = menu.text_input("Enter a description for your segment")
        traffic_type = core_selectors.selection_traffic_type(workspace["id"])

        segments_api.create_segment(workspace["id"], traffic_type["name"], segment_name, segment_description)

        create_segment_in_all_environments(workspace, segment_name)
        menu.success_message("Your segment has been created!")
    except Exception as exc:
        menu.error_message("Could not create segment\n" + str(exc))

def create_segment_in_all_environments(workspace, segment_name):
    environments = environments_api.list_environments(workspace["id"])
    for environment in environments:
        segments_api.activate_segment(segment_name, environment['name'])

def manage_segment(workspace, segment_name):
    while True:
        environments = environments_api.list_environments(workspace["id"])

        options = []
        for environment in environments:
            definition = get_instance(workspace, segment_name, environment)
            option = environment
            if definition == None:
                option["option_name"] = "Create in " + option["name"]
            else:
                option["option_name"] = "Manage in " + option["name"]
            option["operation"] = lambda bound_option=option: manage_instance(workspace, segment_name, bound_option)
            options.append(option)
        options.append({"option_name": "Delete segment", "operation": lambda: delete_segment(workspace, segment_name), "go_back": True})
        options.append({"option_name": "Go back", "go_back": True})
        title = "Managing segment: " + segment_name

        _, go_back = menu.select_operation(title, options)
        if go_back:
            return

def delete_segment(workspace, segment_name):
    title = "Are you sure?"
    options = [
        {"option_name": "Yes", "operation": lambda: segments_api.delete_segment(workspace["id"], segment_name)},
        {"option_name": "No", "go_back": True}
    ]
    menu.select_operation(title, options)

def get_instance(workspace, segment_name, environment):
    try:
        return segments_api.get_segment(workspace["id"], segment_name, environment["name"])
    except Exception as _:
        return None

def manage_instance(workspace, segment_name, environment):
    while True:
        segment = get_instance(workspace, segment_name, environment)
        if segment == None:
            segments_api.activate_segment(segment_name, environment['name'])
        else:
            title = "Managing " + segment["trafficType"]["name"] + " segment \"" + segment_name + "\" in " + environment["name"]

            options = []
            # options.append({"option_name": "Show keys", "operation": lambda: show_keys(segment_name, environment)})
            # options.append({"option_name": "Add keys", "operation": lambda: add_keys(segment_name, environment)})
            # options.append({"option_name": "Remove keys", "operation": lambda: remove_keys(segment_name, environment)})
            # options.append({"option_name": "Upload CSV", "operation": lambda: upload_csv(segment_name, environment)})
            options.append({"option_name": "Go back", "go_back": True})

            _, go_back = menu.select_operation(title, options)
            if go_back:
                return

def show_keys(segment_name, environment):
    page = 0
    while True:
        keys = segments_api.get_segment_keys(segment_name, environment["name"], page)
        print(keys)

def add_keys(segment_name, environment):
    pass

def remove_keys(segment_name, environment):
    pass

def upload_csv(segment_name, environment):
    pass
