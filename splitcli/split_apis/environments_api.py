from splitcli.split_apis import http_client

def environment_url(workspace_id):
    return f"environments/ws/{workspace_id}"

def list_environments(workspace_id):
    path = environment_url(workspace_id)
    return http_client.get(path)

def get_environment(workspace_id, name):
    environments = list_environments(workspace_id)
    environments = list(filter(lambda x: x['name'] == name, environments))
    if len(environments) == 0:
        return None
    else:
        return environments[0]