from os import ttyname
from splitio import workspaces as workspace_client
from splitio import environments as environment_client
from splitio import traffic_types as traffic_types_client
from pick import pick


def selection_environment(workspace_id):
    environments = environment_client.list_environments(workspace_id)
    if len(environments) == 1:
        environment = environments[0]["name"]
        print(f"The only environment is {environment}")
        return environments[0]
    title = 'Please select your environment'
    environment, index = pick(
        environments, title, options_map_func=lambda env: env['name'])
    return environment


def selection_traffic_type(workspace_id):
    traffic_types = traffic_types_client.list_traffic_types(workspace_id)
    if len(traffic_types) == 1:
        traffic_type = traffic_types[0]["name"]
        print(f"The only traffic type is {traffic_type}")
        return traffic_types[0]
    title = 'Please select your traffic type'
    traffic_type, index = pick(
        traffic_types, title, options_map_func=lambda tt: tt['name'])
    return traffic_type


def selection_workspace():
    workspaces = workspace_client.list_workspaces()
    if len(workspaces) == 1:
        workspace = workspaces[0]["name"]
        print(f"The only workspace is {workspace}")
        return workspaces[0]
    title = 'Please select your workspace'
    workspace, index = pick(
        workspaces, title, options_map_func=lambda ws: ws['name'])
    return workspace
