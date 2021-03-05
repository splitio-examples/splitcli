import inquirer

from ux.text import colored, get_color

def error_message(message):
    print(colored(message,"red"))

def info_message(message):
    print(colored(message,"split_blue_light"))

def success_message(message):
    print(colored(message,"split_green"))

def warn_message(message):
    print(colored(message,"split_yellow"))

def option_unavailable():
    error_message("Option unavailable")

def select_strings(title, options):
    options = list(map(set_name, list(options)))
    return select(title, options)

def select(title, options, name_field="option_name"):
    options = list(map(set_operation, list(options)))
    return select_operation(title, options, name_field=name_field)

def set_name(option):
    return {"option_name": option}

def set_operation(option):
    option.update({"operation": lambda: option})
    return option

def select_operation(title, options, name_field="option_name"):
    option_tuples = [ (option[name_field],option) for option in options ]
    questions = [
        inquirer.List('result',
            message=colored(title,"split_green"),
            choices=option_tuples)
    ]
    answers = inquirer.prompt(questions, theme=theme)
    selection = answers['result']
    result = selection["operation"]() if "operation" in selection else None
    return (result, selection.get("go_back", False))

def text_input(title):
    questions = [ inquirer.Text('result',message=title) ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers["result"]

def password_input(title):
    questions = [ inquirer.Password('result',message=title) ]
    answers = inquirer.prompt(questions, theme=theme)
    return answers["result"]

def split_theme():
    theme_dict = {
        "Question": {"mark_color": get_color("split_green"), "brackets_color": get_color("split_yellow")},
        "List": {"selection_color": get_color("split_blue_light"), "selection_cursor": ">"},
    }
    return inquirer.themes.load_theme_from_dict(theme_dict)

theme = split_theme()