from splitio import workspaces_api

def selection_environment():
    # todo: add selection
    return "Prod-Default"

def selection_traffic_type():
    # todo: add selection
    return "user"

def selection_workspace():
    # todo: add selection
    workspace = workspaces_api.get_workspace('Default')
    if workspace == None:
        print("ERROR")
        return None
    return workspace