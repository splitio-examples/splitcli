from splitio import workspaces_api
from splitio import environments_api
from splitio import traffic_types_api
from pick import pick


def selection_environment(workspace_id):
    environments = environments_api.list_environments(workspace_id)
    if len(environments) == 1:
        environment = environments[0]["name"]
        return environments[0]
    title = 'Please select your environment'
    environment,_ = pick(environments, title, options_map_func=lambda env: env['name'])
    return environment

def selection_traffic_type(workspace_id):
    traffic_types = traffic_types_api.list_traffic_types(workspace_id)
    if len(traffic_types) == 1:
        traffic_type = traffic_types[0]["name"]
        return traffic_types[0]
    title = 'Please select your traffic type'
    traffic_type,_ = pick(traffic_types, title, options_map_func=lambda tt: tt['name'])
    return traffic_type

def selection_workspace():
    workspaces = workspaces_api.list_workspaces()
    if len(workspaces) == 1:
        workspace = workspaces[0]["name"]
        return workspaces[0]
    title = 'Please select your workspace'
    workspace,_ = pick(workspaces, title, options_map_func=lambda ws: ws['name'])
    return workspace
