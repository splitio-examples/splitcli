import requests

from accounts.user import User

def create_account():
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
            user.write()
            print(
                "Account Successfully Created, Wrote to Config File. Here is your email and password. Save it")
            print(
                f"email:{okta_response_data['email']}, password:{okta_response_data['password']}")
        else:
            print("error")