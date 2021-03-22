from splitcli.split_apis import workspaces_api, environments_api, traffic_types_api
from splitcli.ux import menu


def selection_environment(workspace_id):
    environments = environments_api.list_environments(workspace_id)
    if len(environments) == 1:
        environment = environments[0]["name"]
        return environments[0]
    
    title = 'Please select your environment'
    environment = menu.select(title, environments, name_field="name")
    return environment

def selection_traffic_type(workspace_id):
    traffic_types = traffic_types_api.list_traffic_types(workspace_id)
    if len(traffic_types) == 1:
        traffic_type = traffic_types[0]["name"]
        return traffic_types[0]
    title = 'Please select your traffic type'
    traffic_type = menu.select(title, traffic_types, name_field="name")
    return traffic_type

def selection_workspace():
    workspaces = workspaces_api.list_workspaces()
    if len(workspaces) == 1:
        workspace = workspaces[0]["name"]
        return workspaces[0]
    title = 'Please select your workspace'
    workspace = menu.select(title, workspaces, name_field="name")
    return workspace
