from urllib.parse import urlencode

from splitcli.split_apis import http_client

# URLs

def users_url():
    return f"users"

def user_url(user_id):
    base_url = users_url()
    return f"{base_url}/{user_id}"

def invite_user(email, group_ids):
    groups = list(map(lambda x: {"id":x, "type":"group"}, group_ids))
    content = {
        "email": email,
        "groups":groups
    }
    http_client.post(users_url(), content)

def list_users(status=None,group_id=None):
    all_users = []
    next_marker = None
    # Stop once a batch is smaller than the limit
    while True:
        result = list_users_batch(next_marker, status, group_id)
        next_marker = result['nextMarker']
        data = result['data']
        if len(data) != 0:
            all_users.extend(data)
        if next_marker is None:
            break
    return all_users

def list_users_batch(next=None, status=None, group_id=None):
    path = users_url()
    query = {}
    if next is not None:
        query["after"] = next
    if status is not None:
        query["status"] = status
    if group_id is not None:
        query["group_id"] = group_id
    if query:
        path += f"?{urlencode(query)}"
    return http_client.get(path)

def get_user_by_email(email):
    users = list_users(status="ACTIVE")
    match = list(filter(lambda x: x['email'] == email, users))
    if len(match) == 1:
        return match[0]
    else:
        return None

def get_user(user_id):
    path = user_url(user_id)
    return http_client.get(path)