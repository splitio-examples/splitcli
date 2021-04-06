from splitcli.split_apis import http_client

# URLs

def segment_base_url(workspace_id):
    return f"segments/ws/{workspace_id}"

def segment_environment_url(workspace_id, environment_name):
    base_url = segment_base_url(workspace_id)
    return f"{base_url}/environments/{environment_name}"

def segment_create_url(workspace_id, traffic_type_name):
    base_url = segment_base_url(workspace_id)
    return f"{base_url}/trafficTypes/{traffic_type_name}"

def segment_metadata_url(workspace_id, segment_name):
    base_url = segment_base_url(workspace_id)
    return f"{base_url}/{segment_name}"

def segment_instance_url(segment_name, environment_name):
    return f"segments/{environment_name}/{segment_name}"

def segment_action_url(segment_name, environment_name, action):
    base_url = segment_instance_url(segment_name, environment_name)
    return f"{base_url}/{action}"

# Segment Metadata

def list_segments(workspace_id):
    all_segments = []
    offset, limit = (0, 20)
    # Stop once a batch is smaller than the limit
    while len(all_segments) % limit == 0:
        result = list_segments_batch(workspace_id, offset, limit)
        if len(result) != 0:
            all_segments.extend(result)
        else:
            break
        offset += limit

    return all_segments

def list_segments_batch(workspace_id, offset, limit):
    path = segment_base_url(workspace_id) + f"?offset={offset}&limit={limit}"
    return http_client.get(path)['objects']

def list_segments_environment(workspace_id, environment_name):
    all_segments = []
    offset, limit = (0, 20)
    # Stop once a batch is smaller than the limit
    while len(all_segments) % limit == 0:
        result = list_segments_environment_batch(workspace_id, environment_name, offset, limit)
        if len(result) != 0:
            all_segments.extend(result)
        else:
            break
        offset += limit
            
    return all_segments

def list_segments_environment_batch(workspace_id, environment_name, offset, limit):
    path = segment_environment_url(workspace_id, environment_name) + f"?offset={offset}&limit={limit}"
    return http_client.get(path)['objects']

def create_segment(workspace_id, traffic_type_name, segment_name, segment_description):
    path = segment_create_url(workspace_id, traffic_type_name)
    content = {
        "name":  segment_name,
        "description": segment_description
    }
    result = http_client.post(path, content)
    return result

def delete_segment(workspace_id, segment_name):
    path = segment_metadata_url(workspace_id, segment_name)
    return http_client.delete(path)

def delete_all_segments(workspace_id):
    segments = list_segments(workspace_id)
    for segment in segments:
        delete_segment(workspace_id, segment['name'])

def get_segment(workspace_id, segment_name, environment_name):
    segments = list_segments_environment(workspace_id, environment_name)
    result = list(filter(lambda x: x['name'] == segment_name, segments))
    if len(result) == 1:
        return result[0]
    else:
        return None

def activate_segment(segment_name, environment_name):
    path = segment_instance_url(segment_name, environment_name)
    return http_client.post(path)

def deactivate_segment(segment_name, environment_name):
    path = segment_instance_url(segment_name, environment_name)
    return http_client.delete(path)

def get_segment_keys(segment_name, environment_name, page=0):
    limit = 100
    offset = page * limit
    path = segment_action_url(segment_name, environment_name, "keys") + f"?offset={offset}&limit={limit}"
    return http_client.get(path)

def add_segment_keys(segment_name, environment_name, keys, replace=False, comment=""):
    content = {
        "keys": keys,
        "comment": comment
    }
    path = segment_action_url(segment_name, environment_name, "uploadKeys")
    if replace:
        path += "?replace"
    return http_client.put(path, content)

def upload_segment_keys(segment_name, environment_name, file_path, replace=False):
    path = segment_action_url(segment_name, environment_name, "upload")
    if replace:
        path += "?replace"
    return http_client.put(path)

def remove_segment_keys(segment_name, environment_name, keys, comment=""):
    content = {
        "keys": keys,
        "comment": comment
    }
    path = segment_action_url(segment_name, environment_name, "removeKeys")
    return http_client.put(path, content)