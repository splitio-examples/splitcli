from splitio import http_client

def kill_split_in_environment(workspace_id, environment_name, split_name):
    path = f"splits/ws/{workspace_id}/{split_name}/environments/{environment_name}/kill"
    http_client.post(path, None)

def get_split(workspace_id, split_name, environment_name):
    path = "splits/ws/{workspace_id}/{split_name}/environments/{environment_name}"
    return http_client.get(path)

def create_split(workspace_id, traffic_type_name, split_name, split_description):
    path = "splits/ws/{workspace_id}/trafficTypes/{traffic_type_name}"
    content = {
        "name":  split_name,
        "description": split_description
    }
    result = http_client.post(path, content)
    return result

def create_split_in_environment(workspace_id, environment_name, split_name, split_data):
    path = "splits/ws/{workspace_id}/{split_name}/environments/{environment_name}"
    content = {
        "name":  split_name,
        "description": split_description
    }
    result = http_client.post(path, content)
    return result