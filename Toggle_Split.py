from Ramp_Split import rampSplit
import requests
from decouple import config
from Create_Split import workspace_id, split_name, split_description


def toggleSplit(comment):

    response = requests.post(
        f"https://api.split.io/internal/api/v2/splits/ws/{workspace_id}/{split_name}/environments/<ENVIRONMENT_NAME_OR_ID>", headers={
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + config('ADMIN_API_KEY')
        }, json={
            "name":  split_name,
            "description": split_description
        })

    return rampSplit(0, comment)
