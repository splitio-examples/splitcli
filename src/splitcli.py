from termcolor import colored
from art import text2art
from pick import pick
import sys

from splitio_selectors.split_selectors import manage_splits
from accounts.user import get_user, sign_in
from accounts import signup
import config

def initial_prompt():
    # Infinite loop is stopped by exit option
    while True:
        user = get_user()
        if user != None:
            knownUserPrompt(user)
        else:
            newUserPrompt()

def knownUserPrompt(user):
    options = [
        { "name": "Manage Splits", "operation": manage_splits },
        { "name": "Log Out", "operation": lambda: user.delete() },
        { "name": "Exit", "operation": exit }
    ]
    title = text2art(f"Hi {user.firstname}!!")
    selection,_ = pick(options, title, options_map_func=lambda x: x['name'])
    selection['operation']()

def newUserPrompt():
    options = [
        { "name": "No, I need to create an account", "operation": lambda: signup.create_account() },
        { "name": "Yes, take me to sign in", "operation": lambda: sign_in() },
        { "name": "Exit", "operation": exit }
    ]
    title = f"Welcome to Split! Do you have an existing account?"
    selection,_ = pick(options, title, options_map_func=lambda x: x['name'])
    selection['operation']()

def main():
    major_required = 3
    minor_required = 6

    if sys.version_info.major < major_required or sys.version_info.minor < minor_required:
        print(f"Minimum version requirement is: {major_required}.{minor_required}. Your version is: {sys.version_info.major}.{sys.version_info.minor}")
        exit()

    initial_prompt()

main()