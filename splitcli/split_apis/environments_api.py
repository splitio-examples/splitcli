from splitcli.split_apis import http_client


def environment_url(workspace_id):
    return f"environments/ws/{workspace_id}"


def list_environments(workspace_id):
    path = environment_url(workspace_id)
    return http_client.get(path)
