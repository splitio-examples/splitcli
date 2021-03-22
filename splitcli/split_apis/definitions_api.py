from splitcli.split_apis import http_client
from splitcli.split_apis.splits_api import split_metadata_url

def split_url(workspace_id, split_name, environment_name):
    base_url = split_metadata_url(workspace_id, split_name)
    return f"{base_url}/environments/{environment_name}"

def split_action_url(workspace_id, split_name, environment_name, action):
    base_url = split_url(workspace_id, split_name, environment_name)
    return f"{base_url}/{action}"

# Split in Environment

def get(workspace_id, environment_name, split_name):
    path = split_url(workspace_id, split_name, environment_name)
    return http_client.get(path)

def create(workspace_id, environment_name, split_name, split_data):
    path = split_url(workspace_id, split_name, environment_name)
    result = http_client.post(path, split_data)
    return result

def full_update(workspace_id, environment_name, split_name, split_data):
    path = split_url(workspace_id, split_name, environment_name)
    result = http_client.put(path, split_data)
    return result

def delete(workspace_id, environment_name, split_name):
    path = split_url(workspace_id, split_name, environment_name)
    http_client.delete(path)

def kill(workspace_id, environment_name, split_name):
    path = split_action_url(workspace_id, split_name, environment_name, "kill")
    http_client.post(path, None)

def restore(workspace_id, environment_name, split_name):
    path = split_action_url(workspace_id, split_name, environment_name, "restore")
    http_client.post(path, None)