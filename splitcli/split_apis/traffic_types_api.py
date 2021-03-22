from splitcli.split_apis import http_client


def traffic_types_url(workspace_id):
    return f"trafficTypes/ws/{workspace_id}"

def list_traffic_types(workspace_id):
    path = traffic_types_url(workspace_id)
    return http_client.get(path)

def get_traffic_type(workspace_id, name):
    traffic_types = list_traffic_types(workspace_id)
    traffic_types = list(filter(lambda x: x['name'] == name, traffic_types))
    if len(traffic_types) == 0:
        return None
    else:
        return traffic_types[0]