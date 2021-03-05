from splitio import workspaces_api
from splitio import environments_api
from splitio import traffic_types_api
from ux.menu import select


def selection_environment(workspace_id):
    environments = environments_api.list_environments(workspace_id)
    if len(environments) == 1:
        environment = environments[0]["name"]
        return environments[0]
    
    title = 'Please select your environment'
    environment = select(title, environments, name_field="name")
    return environment

def selection_traffic_type(workspace_id):
    traffic_types = traffic_types_api.list_traffic_types(workspace_id)
    if len(traffic_types) == 1:
        traffic_type = traffic_types[0]["name"]
        return traffic_types[0]
    title = 'Please select your traffic type'
    traffic_type = select(title, traffic_types, name_field="name")
    return traffic_type

def selection_workspace():
    workspaces = workspaces_api.list_workspaces()
    if len(workspaces) == 1:
        workspace = workspaces[0]["name"]
        return workspaces[0]
    title = 'Please select your workspace'
    workspace = select(title, workspaces, name_field="name")
    return workspace
