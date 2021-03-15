from splitcli.split_apis import http_client

def list_workspaces():
    path = 'workspaces'
    return http_client.get(path)['objects']

def get_workspace(name):
    workspaces = list_workspaces()
    workspaces = list(filter(lambda x: x['name'] == name, workspaces))
    if len(workspaces) == 0:
        return None
    else:
        return workspaces[0]