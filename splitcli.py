from termcolor import colored
from art import *

from selectors.split_selectors import *
from accounts.user import get_user
from accounts import signup

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


def initial_prompt():
    user = get_user()
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
        selection_create_split()
    elif selection == "3":
        selection_kill_split()
    elif selection == "4":
        selection_create_split()
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
        signup.create_account()
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
