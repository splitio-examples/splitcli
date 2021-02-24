from splitio import http_client

# URLs

def split_base_url(workspace_id):
    return f"splits/ws/{workspace_id}"

def split_metadata_url(workspace_id, traffic_type_name):
    base_url = split_base_url(workspace_id)
    return f"{base_url}/trafficTypes/{traffic_type_name}"

def split_url(workspace_id, split_name, environment_name):
    base_url = split_base_url(workspace_id)
    return f"{base_url}/{split_name}/environments/{environment_name}"

def split_action_url(workspace_id, split_name, environment_name, action):
    base_url = split_url(workspace_id, split_name, environment_name)
    return f"{base_url}/{action}"

# Functions

def kill_split_in_environment(workspace_id, environment_name, split_name):
    path = split_action_url(workspace_id, split_name, environment_name, "kill")
    http_client.post(path, None)

def get_split(workspace_id, split_name, environment_name):
    path = split_url(workspace_id, split_name, environment_name)
    return http_client.get(path)

def create_split(workspace_id, traffic_type_name, split_name, split_description):
    path = split_metadata_url(workspace_id, traffic_type_name)
    content = {
        "name":  split_name,
        "description": split_description
    }
    result = http_client.post(path, content)
    return result

def create_split_in_environment(workspace_id, environment_name, split_name, split_data):
    path = split_url(workspace_id, split_name, environment_name)
    content = {
        "name":  split_name,
        "description": split_description
    }
    result = http_client.post(path, content)
    return result