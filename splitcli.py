import requests


def createaccount():
    firstname = input("Enter Your First Name: ")
    lastname = input("Enter Your Last Name: ")
    email = input("Enter Your Email Address: ")

    response = requests.post(
        'https://api.hsforms.com/submissions/v3/integration/submit/3371296/8d489e14-08ee-4e78-920e-bb211ea6c9c9', json={"fields": [
            {
                "name": "firstname",
                "value": firstname
            },
            {
                "name": "lastname",
                "value": lastname
            },
            {
                "name": "email",
                "value": email
            }
        ]})

    response.status_code
    response.json()

    if response.status_code != 200:
        print(response.json())
    else:
        print("Your accout has been created! Please check your email.")


def initial_prompt():
    print("Welcome to Split! Please Make A Selection:")
    print("1. Create Account")
    print("2. Exit")
    selection = input("Selection: ")
    if selection == "1":
        createaccount()
        initial_prompt()
    elif selection == "2":
        exit()
    else:
        print(f"Invalid selection: {selection}")
        initial_prompt()


initial_prompt()
