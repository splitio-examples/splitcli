import json
import os

config_file = "config.txt"

user_singleton = None
def get_user():
    global user_singleton
    if user_singleton == None:
        user_singleton = load_user(config_file)
    return user_singleton

def load_user(filename):
    try:
        with open(filename, 'r') as f:
            dictionary = json.load(f)
            return User(filename, dictionary["adminapi"], dictionary["orgID"], dictionary["userID"], dictionary["firstname"], dictionary["lastname"], dictionary["email"], dictionary["phone"])
    except:
        return None

class User(object):    
    def __init__(self, filename, adminapi: str, orgID: str, userID: str, firstname: str, lastname: str, email: str, phone: str):
        self.filename = filename
        self.adminapi = adminapi
        self.orgID = orgID
        self.userID = userID
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone

    def __str__(self):
        return json.dumps(self.__dict__)

    def write(self):
        with open(self.filename, 'w') as f:
            json.dump(self.__dict__, f)

    def delete(self):
        global user_singleton
        if os.path.exists(self.filename):
            os.remove(self.filename)
            user_singleton = None