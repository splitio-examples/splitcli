import requests
from pick import pick
from termcolor import colored


def createSplit():
    split_name = input("Enter a name for your Split: ")
    split_description = input("Enter a description for your Split: ")
    split_traffic_type = "Choose a traffic type"
    traffic_type_options = ["user", "account", "anon"]
    traffic_type_option, index = pick(traffic_type_options, split_traffic_type)
    create_split_response = requests.post(
        f"https://api.split.io/internal/api/v2/splits/ws/f8aa2660-3f31-11eb-be37-12b057418355/trafficTypes/{traffic_type_option}", headers: {
            'Content-Type': 'application/json',
            'Authorization': PROCESS.ENV.ADMINAPIKEY
        }, json={"fields": [
            {
                 "name": "name",
                 "value": split_name
                 },
            {
                "name": "description",
                "value": split_description
            }

        ]})

    create_split_response.status_code
    create_split_response.json()

    if create_split_response.status_code != 200:
        print(create_split_response.json())
    else:
        print(colored("Your Split has been created!"), "green")
