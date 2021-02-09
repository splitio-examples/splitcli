import requests
from User import User
from termcolor import colored
from Create_Split import createSplit
from art import *

config_file = "config.txt"


def createaccount():
    firstname = input("Enter Your First Name: ")
    lastname = input("Enter Your Last Name: ")
    email = input("Enter Your Email Address: ")
    phone = input("Enter Your 10 Digit Phone Number: ")
    user = User(config('ADMIN_API_KEY'), config('ORG_ID'), "userID",
                firstname, lastname, email, phone)
    user.write(config_file)
    print("Setting up your account...")
    split_response = requests.post(
        'https://split-cli-backend.herokuapp.com/api/v1/register-for-split', json={"fields": [
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
            'https://split-cli-backend.herokuapp.com/api/v1/verify-factor', json={"fields": [
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
                }
            ]}
        )


def signin():
    split_apikey = input("Enter Your Split API Key")
    signin_response = requests.post('SPLITSIGNIN URL', json={"fields": [
        {
            "name": "apikey",
            "value": split_apikey
        }
    ]})

    signin_response.status_code
    signin_response.json()

    if signin_response.status_code != 200:
        print(signin_response.json())
    else:
        print("You are signed in")
        initial_prompt()


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
    print(colored("2. Log Out", 'red'))
    print(colored("3. Exit", 'blue'))
    selection = input("Selection: ")
    if selection == "1":
        createSplit()
    elif selection == "2":
        user.delete()
        initial_prompt()
    elif selection == "3":
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
