import json
import os
import config

from ux.menu import text_input, password_input

user_singleton = None
def get_user():
    global user_singleton
    if user_singleton == None:
        user_singleton = load_user()
    return user_singleton

def load_user():
    try:
        with open(config.config_file, 'r') as f:
            dictionary = json.load(f)
            return User(dictionary["adminapi"], dictionary["orgID"], dictionary["userID"], dictionary["firstname"], dictionary["lastname"], dictionary["email"])
    except:
        return None

def sign_in():
    firstname = text_input("Enter your first name: ")
    split_apikey = password_input("Enter a Split Admin API Token: ")
    user = User(split_apikey, "", "", firstname, "", "")
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
        global user_singleton
        if os.path.exists(config.config_file):
            os.remove(config.config_file)
            user_singleton = None