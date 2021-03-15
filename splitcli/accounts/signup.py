import requests

from splitcli import config
from splitcli.ux import menu
from splitcli.accounts.user import User


def verify_and_complete(firstname, lastname, email):
    confirmation_code = menu.text_input(
        "Please enter the 6 digit confirmation code sent to your phone"
    )
    menu.info_message("Processing account creation...")
    menu.info_message("This could take up to one minute.")
    # TODO - validate confirmation code is a 6-digit number
    verify_response = requests.post(
        f"{config.SPLIT_CLI_BACKEND_BASE_URL}/verify-and-complete", json={"fields": [
            {"name": "firstname", "value": firstname},
            {"name": "lastname", "value": lastname},
            {"name": "email", "value": email},
            {"name": "passCode", "value": confirmation_code}
        ]}
    )
    return verify_response


def create_account():
    firstname = menu.text_input("Enter Your First Name")
    lastname = menu.text_input("Enter Your Last Name")
    email = menu.text_input("Enter Your Email Address")
    phone = menu.text_input("Enter Your 10 Digit Phone Number")

    menu.info_message("Setting up your account...")
    create_response = requests.post(
        f"{config.SPLIT_CLI_BACKEND_BASE_URL}/create-and-enroll-user", json={"fields": [
            {"name": "firstname", "value": firstname},
            {"name": "lastname", "value": lastname},
            {"name": "email", "value": email},
            {"name": "phone", "value": phone}
        ]})

    if create_response.status_code != 200:
        menu.error_message(create_response.json())
        exit()

    status = 403
    while status == 403:
        verify_response = verify_and_complete(firstname, lastname, email)
        status = verify_response.status_code
        if (status == 403):
            menu.warn_message("Incorrect confirmation code. Please try again")

    if verify_response.status_code != 200:
        menu.error_message(verify_response.json())
        exit()

    verify_response_json = verify_response.json()
    user = User(
        verify_response_json["apiToken"],
        verify_response_json["orgId"], verify_response_json["userId"],
        firstname, lastname, email
    )
    user.write()
    password = verify_response_json["password"]
    menu.info_message(f"\nYour admin api key has been written to: {config.config_file}.")
    menu.info_message(f"Your email is: {email} and your assigned password is: {password}.")
    menu.info_message("Make note of your password as it will not be repeated. You can change your password by logging in to: https://app.split.io")
