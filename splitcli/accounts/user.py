import json
import os
import splitcli.config

from splitcli.split_apis import users_api
from splitcli.ux import menu

_user_singleton = None


def get_user():
    global _user_singleton
    if _user_singleton == None:
        set_user(load_user())
    return _user_singleton


def set_user(new_user):
    global _user_singleton
    _user_singleton = new_user


def load_user():
    try:
        with open(config.config_file, 'r') as f:
            dictionary = json.load(f)
            return User(dictionary["adminapi"], dictionary["orgID"], dictionary["userID"], dictionary["firstname"], dictionary["lastname"], dictionary["email"])
    except:
        return None

def sign_in():
    email = menu.text_input("Enter your email")
    menu.info_message("To find your Admin API Key, follow the directions here:")
    menu.info_message("https://www.youtube.com/watch?v=80Bz2ZcZUrs")
    split_apikey = menu.password_input("Enter your Split Admin API Key")
    user = User(split_apikey, "", "", "", "", email)
    set_user(user)

    # Check user
    active_user = users_api.get_user_by_email(email)
    if active_user != None:
        user.firstname = active_user['name']
    else:
        user.firstname = email
        menu.warn_message("Email does not exist in organization")

    user.write()

    return user


class User(object):
    def __init__(self, adminapi: str, orgID: str, userID: str, firstname: str, lastname: str, email: str):
        self.adminapi = adminapi
        self.orgID = orgID
        self.userID = userID
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def __str__(self):
        return json.dumps(self.__dict__)

    def write(self):
        with open(config.config_file, 'w') as f:
            json.dump(self.__dict__, f)

    def delete(self):
        global _user_singleton
        if os.path.exists(config.config_file):
            os.remove(config.config_file)
            _user_singleton = None
