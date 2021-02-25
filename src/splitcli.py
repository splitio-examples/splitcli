from termcolor import colored
from art import text2art
from pick import pick

from selectors.split_selectors import manage_splits
from accounts.user import get_user
from accounts import signup

SPLIT_CLI_BACKEND_URI = "https://split-cli-backend.herokuapp.com"
SPLIT_CLI_BACKEND_API_URI = "/api/v1"
SPLIT_CLI_BACKEND_BASE_URL = f"{SPLIT_CLI_BACKEND_URI}{SPLIT_CLI_BACKEND_API_URI}"

# def sign_in():
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
    options = [
        { "name": "Manage Splits", "operation": manage_splits },
        { "name": "Log Out", "operation": lambda: logout(user) },
        { "name": "Exit", "operation": exit }
    ]
    title = text2art(f"Hi {user.firstname}!!")
    selection,_ = pick(options, title, options_map_func=lambda x: x['name'])
    selection['operation']()

    initial_prompt()

def logout(user):
    user.delete()
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
        # sign_in()
        initial_prompt()
    elif selection == "3":
        exit()
    else:
        print(f"Invalid selection: {selection}")
        initial_prompt()

def main():
    major_required = 3
    minor_required = 6

    if sys.version_info.major < major_required or sys.version_info.minor < minor_required:
        print(f"Minimum version requirement is: {major_required}.{minor_required}. Your version is: {sys.version_info.major}.{sys.version_info.minor}")
        exit()

    parser = argparse.ArgumentParser(description='optional baseUrl')
    parser.add_argument('--baseUrl', help='optional base url')
    args = parser.parse_args()
    if args.baseUrl is not None:
        global SPLIT_CLI_BACKEND_URI
        global SPLIT_CLI_BACKEND_BASE_URL
        SPLIT_CLI_BACKEND_URI = args.baseUrl
        SPLIT_CLI_BACKEND_BASE_URL = f"{SPLIT_CLI_BACKEND_URI}{SPLIT_CLI_BACKEND_API_URI}"
        print(f"Working with base url: {SPLIT_CLI_BACKEND_URI}")

    initial_prompt()