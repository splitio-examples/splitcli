from splitcli.ux import menu
from splitcli.accounts import user
from splitcli.split_apis import users_api

def sign_in():
    email = menu.text_input("Enter your email")
    menu.info_message("To find your Admin API Key, follow the directions here:")
    menu.info_message("https://www.youtube.com/watch?v=80Bz2ZcZUrs")
    split_apikey = menu.password_input("Enter your Split Admin API Key")
    new_user = user.User(split_apikey, "", "", "", "", email)
    user.set_user(new_user)

    # Check user
    active_user = users_api.get_user_by_email(email)
    if active_user != None:
        new_user.firstname = active_user['name']
    else:
        new_user.firstname = email
        menu.warn_message("Email does not exist in organization")

    new_user.write()

    return new_user