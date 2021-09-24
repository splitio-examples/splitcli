from art import text2art
import argparse
import sys

from splitcli.splitio_selectors import split_selectors, segment_selectors, metric_selectors, organization_selectors
from splitcli.accounts import signup, user, signin
from splitcli.ux import menu, text
from splitcli import config

def initial_prompt_deprecate():
    print('''
A few months ago Split Skunkworks (aka developer advocacy) embarked on an 
experiment to create a command line interface (CLI) tool to provision and 
interact with Split accounts. The experiment was a success and we are now 
assessing putting formal engineering muscle behind it. For now, we are taking 
it offline until such time as we are ready to release a fully supported version.
    ''')
    exit()

def initial_prompt():
    # Infinite loop is stopped by exit option
    while True:
        current_user = user.get_user()
        if current_user is not None:
            knownUserPrompt(current_user)
        else:
            newUserPrompt()

def knownUserPrompt(user):
    menu.info_message(text2art(f"Hi {user.firstname}!!!"))
    options = [
        {"option_name": "Manage Splits", "operation": split_selectors.manage_splits},
        {"option_name": "Manage Segments", "operation": segment_selectors.manage_segments},
        # {"option_name": "Manage Metrics", "operation": metric_selectors.manage_metrics},
        # {"option_name": "Manage Organization", "operation": organization_selectors.manage_organization},
        {"option_name": "Log Out", "operation": lambda: user.delete()},
        {"option_name": "Exit", "operation": exit}
    ]
    title = "Select"
    menu.select_operation(title, options)

def newUserPrompt():
    menu.info_message(text2art(f"Welcome to Split!"))
    options = [
        {"option_name": "No, I need to create an account",
            "operation": lambda: signup.create_account()},
        {"option_name": "Yes, take me to sign in", "operation": lambda: signin.sign_in()},
        {"option_name": "Exit", "operation": exit}
    ]
    title = f"Do you have an existing account?"
    menu.select_operation(title, options)

def main():
    major_required = 3
    minor_required = 6

    if sys.version_info.major < major_required or sys.version_info.minor < minor_required:
        menu.error_message(
            f"Minimum version requirement is: {major_required}.{minor_required}. Your version is: {sys.version_info.major}.{sys.version_info.minor}")
        exit()

    menu.print_logo()
    initial_prompt_deprecate()

main()
