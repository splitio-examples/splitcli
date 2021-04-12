from splitcli.split_apis import http_client

# URLs

def split_base_url(workspace_id):
    return f"splits/ws/{workspace_id}"

def split_create_url(workspace_id, traffic_type_name):
    base_url = split_base_url(workspace_id)
    return f"{base_url}/trafficTypes/{traffic_type_name}"

def split_metadata_url(workspace_id, split_name):
    base_url = split_base_url(workspace_id)
    return f"{base_url}/{split_name}"

# Split Metadata

def list_splits(workspace_id):
    all_splits = []
    offset, limit = (0, 20)
    # Stop once a batch is smaller than the limit
    while len(all_splits) % limit == 0:
        result = list_splits_batch(workspace_id, offset, limit)
        if len(result) != 0:
            all_splits.extend(result)
        else:
            break
        offset += limit

    return all_splits

def list_splits_batch(workspace_id, offset, limit):
    path = split_base_url(workspace_id) + f"?offset={offset}&limit={limit}"
    return http_client.get(path)['objects']

def create_split(workspace_id, traffic_type_name, split_name, split_description):
    path = split_create_url(workspace_id, traffic_type_name)
    content = {
        "name":  split_name,
        "description": split_description
    }
    result = http_client.post(path, content)
    return result

def get_split(workspace_id, split_name):
    path = split_metadata_url(workspace_id, split_name)
    return http_client.get(path)

def delete_split(workspace_id, split_name):
    path = split_metadata_url(workspace_id, split_name)
    return http_client.delete(path)

def delete_all_splits(workspace_id):
    all_splits = list_splits(workspace_id)
    for split in all_splits:
        delete_split(workspace_id, split["name"])
