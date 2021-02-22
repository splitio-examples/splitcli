import json
import os


class User(object):
    def __init__(self, adminApiKey: str, orgId: str, userId: str, firstname: str, lastname: str, email: str):
        self.adminApiKey = adminApiKey
        self.orgId = orgId
        self.userId = userId
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def __str__(self):
        return json.dumps(self.__dict__)

    def write(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.__dict__, f)

    def load(filename):
        try:
            with open(filename, 'r') as f:
                dictionary = json.load(f)
                return User(dictionary["adminApiKey"], dictionary["orgId"], dictionary["userId"], dictionary["firstname"], dictionary["lastname"], dictionary["email"])
        except:
            return None

    def delete(filename):
        if os.path.exists(filename):
            os.remove(filename)
