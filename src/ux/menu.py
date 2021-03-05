import inquirer

from ux.text import colored, get_color

# Logging

def error_message(message):
    print(colored(message,"red"))

def info_message(message):
    print(colored(message,"split_blue_light"))

def success_message(message):
    print(colored(message,"split_green"))

def warn_message(message):
    print(colored(message,"split_yellow"))

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
    if name_field is not None:
        options = [ (option[name_field],option) for option in options ]
    questions = [
        inquirer.List('result',
            message=colored(title,"split_green"),
            choices=options)
    ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers['result']

def checkbox(title, options, selections, name_field=None):
    if name_field is not None:
        options = [ (option[name_field], option) for option in options ]
    questions = [ inquirer.Checkbox('result', message=title, choices=options, default=selections) ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers["result"]

def split_theme():
    theme_dict = {
        "Question": {"mark_color": get_color("split_yellow"), "brackets_color": get_color("split_green")},
        "List": {"selection_color": get_color("split_blue_light"), "selection_cursor": ">"},
    }
    return inquirer.themes.load_theme_from_dict(theme_dict)

theme = split_theme()