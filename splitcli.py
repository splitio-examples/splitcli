import requests
from User import User
from termcolor import colored
from Create_Split import createSplit, create_split, selection_get_split, selection_create_split
from Kill_Split import selection_kill_split
from art import *
from decouple import config

config_file = "config.txt"


def createaccount():
    firstname = input("Enter Your First Name: ")
    lastname = input("Enter Your Last Name: ")
    email = input("Enter Your Email Address: ")
    phone = input("Enter Your 10 Digit Phone Number: ")

    print("Setting up your account...")
    split_response = requests.post(
        'https://split-cli-backend.herokuapp.com/api/v1/create-and-enroll-user', json={"fields": [
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
            },
            {
                "name": "phone",
                "value": phone
            }
        ]})

    split_response.status_code
    split_response.json()

    if split_response.status_code != 200:
        print(split_response.json())
    else:
        confirmation_code = input(
            "Please enter the 6 digit confirmation code sent to your phone: ")
        okta_response = requests.post(
            'https://split-cli-backend.herokuapp.com/api/v1/verify-and-complete', json={"fields": [
                {
                    "name": "userId",
                    "value": split_response.json()["userId"]
                },
                {
                    "name": "factorId",
                    "value": split_response.json()["factorId"]
                },
                {
                    "name": "passCode",
                    "value": confirmation_code
                },
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
            ]}
        )

        okta_response.status_code
        okta_response_data = okta_response.json()

        if okta_response.status_code == 200:
            user = User(okta_response_data["apiToken"], okta_response_data["orgId"], okta_response_data["userId"],
                        firstname, lastname, email, phone)
            user.write(config_file)
            print(
                "Account Successfully Created, Wrote to Config File. Here is your email and password. Save it")
            print(
                f"email:{okta_response_data['email']}, password:{okta_response_data['password']}")
        else:
            print("error")


# def signin():
#     split_apikey = input("Enter Your Split API Key")
#     signin_response = requests.post('SPLITSIGNIN URL', json={"fields": [
#         {
#             "name": "apikey",
#             "value": split_apikey
#         }
#     ]})

#     signin_response.status_code
#     signin_response.json()

#     if signin_response.status_code != 200:
#         print(signin_response.json())
#     else:
#         print("You are signed in")
#         initial_prompt()


def getUser():
    return User.load(config_file)


def initial_prompt():
    user = getUser()
    if user != None:
        knownUserPrompt(user)
    else:
        newUserPrompt()


def knownUserPrompt(user):
    print(colored(text2art(f"Hi {user.firstname}!!"), 'cyan'))
    print(colored("1. Create a Split", 'green'))
    print(colored("2. Ramp a Split", 'yellow'))
    print(colored("3. Kill a Split", 'red'))
    print(colored("4. Promote a Split", 'blue'))
    print(colored("5. Log Out", 'white'))
    print(colored("6. Exit", 'white'))
    selection = input(colored("Selection: ", "cyan"))
    if selection == "1":
        selection_create_split()
    elif selection == "2":
        createSplit()
    elif selection == "3":
        selection_kill_split()
    elif selection == "4":
        createSplit()
    elif selection == "5":
        user.delete()
        initial_prompt()
    elif selection == "6":
        exit()
    else:
        print(f"Invalid selection: {selection}")
        initial_prompt()


def newUserPrompt():
    print("Welcome to Split! Do you have an existing account?")
    print("1. No, I need to create an account")
    print("2. Yes, take me to sign in")
    print("3. Exit")
    selection = input("Selection: ")
    if selection == "1":
        createaccount()
        initial_prompt()
    elif selection == "2":
        sign_in()
        initial_prompt()
    elif selection == "3":
        exit()
    else:
        print(f"Invalid selection: {selection}")
        initial_prompt()


initial_prompt()
