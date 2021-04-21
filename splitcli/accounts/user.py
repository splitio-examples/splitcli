import json
import os

from splitcli import config
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
            print(dictionary)
            return User(dictionary["adminapi"], dictionary["orgID"], dictionary["userID"], dictionary["firstname"], dictionary["lastname"], dictionary["email"])
    except:
        return None

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
