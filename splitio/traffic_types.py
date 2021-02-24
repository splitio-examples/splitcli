from splitio import http_client

# URLs


def traffic_types_url(workspace_id):
    return f"trafficTypes/ws/{workspace_id}"


def list_traffic_types(workspace_id):
    path = traffic_types_url(workspace_id)
    return http_client.get(path)
