import json
import os


class User(object):
    def __init__(self, adminapi: str, orgID: str, userID: str, firstname: str, lastname: str, email: str, phone: str):
        self.adminapi = adminapi
        self.orgID = orgID
        self.userID = userID
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone

    def __str__(self):
        return json.dumps(self.__dict__)

    def write(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.__dict__, f)

    def load(filename):
        try:
            with open(filename, 'r') as f:
                dictionary = json.load(f)
                return User(dictionary["adminapi"], dictionary["orgID"], dictionary["userID"], dictionary["firstname"], dictionary["lastname"], dictionary["email"], dictionary["phone"])
        except:
            return None

    def delete(filename):
        if os.path.exists(filename):
            os.remove(filename)
