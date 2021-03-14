from art import text2art
import argparse
import sys

<<<<<<< HEAD
from splitio_selectors import split_selectors, segment_selectors, metric_selectors, organization_selectors
from accounts import signup, signin, user
=======
from splitio_selectors.split_selectors import manage_splits
from splitio_selectors.segment_selectors import manage_segments
from splitio_selectors.metric_selectors import manage_metrics
from splitio_selectors.organization_selectors import manage_organization
from accounts.user import get_user, sign_in
from accounts import signup
>>>>>>> main
import config
from ux import menu, text


def initial_prompt():
    # Infinite loop is stopped by exit option
    while True:
<<<<<<< HEAD
        current_user = user.get_user()
        if user != None:
            knownUserPrompt(current_user)
=======
        user = get_user()
        if user != None:
            knownUserPrompt(user)
>>>>>>> main
        else:
            newUserPrompt()

def knownUserPrompt(user):
    menu.info_message(text2art(f"Hi {user.firstname}!!!"))
    options = [
<<<<<<< HEAD
        {"option_name": "Manage Splits", "operation": lambda x: split_selectors.manage_splits()},
        {"option_name": "Manage Segments", "operation": lambda x: segment_selectors.manage_segments()},
        {"option_name": "Manage Metrics", "operation": lambda x: metric_selectors.manage_metrics()},
        {"option_name": "Manage Organization", "operation": lambda x: organization_selectors.manage_organization()},
=======
        {"option_name": "Manage Splits", "operation": manage_splits},
        {"option_name": "Manage Segments", "operation": manage_segments},
        {"option_name": "Manage Metrics", "operation": manage_metrics},
        {"option_name": "Manage Organization", "operation": manage_organization},
>>>>>>> main
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
<<<<<<< HEAD
        {"option_name": "Yes, take me to sign in", "operation": lambda: signin.sign_in()},
=======
        {"option_name": "Yes, take me to sign in", "operation": lambda: sign_in()},
>>>>>>> main
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
    initial_prompt()

main()
