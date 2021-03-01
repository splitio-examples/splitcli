import requests
import config

from accounts.user import User


def verify_and_complete(firstname, lastname, email):
    confirmation_code = input(
        "Please enter the 6 digit confirmation code sent to your phone: "
    )
    print("Processing account creation...")
    print("This could take up to one minute.")
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
    firstname = input("Enter Your First Name: ")
    lastname = input("Enter Your Last Name: ")
    email = input("Enter Your Email Address: ")
    phone = input("Enter Your 10 Digit Phone Number: ")

    print("Setting up your account...")
    create_response = requests.post(
        f"{config.SPLIT_CLI_BACKEND_BASE_URL}/create-and-enroll-user", json={"fields": [
            {"name": "firstname", "value": firstname},
            {"name": "lastname", "value": lastname},
            {"name": "email", "value": email},
            {"name": "phone", "value": phone}
        ]})

    if create_response.status_code != 200:
        print(create_response.json())
        exit()

    create_response_json = create_response.json()
    status = 403
    while status == 403:
        verify_response = verify_and_complete(firstname, lastname, email)
        status = verify_response.status_code
        if (status == 403):
            print("Incorrect confirmation code. Please try again")

    if verify_response.status_code != 200:
        print(verify_response.json())
        exit()

    verify_response_json = verify_response.json()
    user = User(
        verify_response_json["apiToken"],
        verify_response_json["orgId"], verify_response_json["userId"],
        firstname, lastname, email
    )
    user.write()
    password = verify_response_json["password"]
    print(f"\nYour admin api key has been written to: {config.config_file}.")
    print(f"Your email is: {email} and your assigned password is: {password}.")
    print("Make note of your password as it will not be repeated. You can change your password by logging in to: https://app.split.io")
