from termcolor import colored
from art import text2art
from ux.menu import select_operation
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
    print(text2art(f"Hi {user.firstname}!!!"))
    options = [
        {"option_name": "Manage Splits", "operation": manage_splits},
        {"option_name": "Log Out", "operation": lambda: user.delete()},
        {"option_name": "Exit", "operation": exit}
    ]
    title = "Select"
    select_operation(title, options)

def newUserPrompt():
    print(text2art(f"Welcome to Split!"))
    options = [
        {"option_name": "No, I need to create an account",
            "operation": lambda: signup.create_account()},
        {"option_name": "Yes, take me to sign in", "operation": lambda: sign_in()},
        {"option_name": "Exit", "operation": exit}
    ]
    title = f"Do you have an existing account?"
    select_operation(title, options)

def main():
    major_required = 3
    minor_required = 6

    if sys.version_info.major < major_required or sys.version_info.minor < minor_required:
        print(
            f"Minimum version requirement is: {major_required}.{minor_required}. Your version is: {sys.version_info.major}.{sys.version_info.minor}")
        exit()

    initial_prompt()

main()
