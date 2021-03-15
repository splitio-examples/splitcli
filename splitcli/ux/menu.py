import inquirer

from splitcli.ux import text

# Logging

def print_logo():
    print(text.split_logo())

def error_message(message):
    print(text.colored(message,"red"))

def info_message(message):
    print(text.colored(message,"split_blue_light"))

def success_message(message):
    print(text.colored(message,"split_green"))

def warn_message(message):
    print(text.colored(message,"split_yellow"))

# Inputs

def input_list(title, validator=lambda t: None):
    items = []
    while True:
        item = text_input(title + " (empty when done)")
        if item == "":
            error = validator(items)
            if error is None:
                break
            else:
                error_message(error)
        else:
            items.append(item)
    return items

def text_input(title):
    questions = [ inquirer.Text('result',message=title) ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers["result"]

def password_input(title):
    questions = [ inquirer.Password('result',message=title) ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers["result"]

def select_operation(title, options, name_field="option_name"):
    selection = select(title, options, name_field=name_field)
    result = selection["operation"]() if "operation" in selection else None
    return (result, selection.get("go_back", False))

def select(title, options, name_field=None):
    print("") # Add some space
    if name_field is not None:
        options = [ (option[name_field],option) for option in options ]
    questions = [
        inquirer.List('result',
            message=text.colored(title,"split_green"),
            choices=options)
    ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers['result']

def checkbox(title, options, selections, name_field=None):
    title += " [space to select]"
    if name_field is not None:
        options = [ (option[name_field], option) for option in options ]
    questions = [ inquirer.Checkbox('result', message=title, choices=options, default=selections) ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers["result"]

theme = inquirer.themes.load_theme_from_dict(text.inquirer_theme())