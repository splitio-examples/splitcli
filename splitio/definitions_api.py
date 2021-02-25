from splitio import http_client
from splitio.splits_api import split_metadata_url

def split_url(workspace_id, split_name, environment_name):
    base_url = split_metadata_url(workspace_id, split_name)
    return f"{base_url}/environments/{environment_name}"

def split_action_url(workspace_id, split_name, environment_name, action):
    base_url = split_url(workspace_id, split_name, environment_name)
    return f"{base_url}/{action}"

# Split in Environment

def get_split_definition(workspace_id, split_name, environment_name):
    path = split_url(workspace_id, split_name, environment_name)
    return http_client.get(path)

def create_split_in_environment(workspace_id, environment_name, split_name, split_dataa):
    path = split_url(workspace_id, split_name, environment_name)
    result = http_client.post(path, split_dataa)
    return result

def kill_split_in_environment(workspace_id, environment_name, split_name):
    path = split_action_url(workspace_id, split_name, environment_name, "kill")
    http_client.post(path, None)

def restore_split_in_environment(workspace_id, environment_name, split_name):
    path = split_action_url(workspace_id, split_name, environment_name, "restore")
    http_client.post(path, None)