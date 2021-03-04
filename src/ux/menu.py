import inquirer

from ux.text import colored, split_color

def output_message(message, option="Continue"):
    print(colored(message,"yellow"))

def select(title, options, name_field="option_name"):
    options = list(map(set_operation, options))
    return select_operation(title, options, name_field=name_field)

def set_operation(option):
    option.update({"operation": lambda: option})
    return option

def select_operation(title, options, name_field="option_name"):
    option_tuples = [ (option[name_field],option) for option in options ]
    questions = [
        inquirer.List('result',
            message=colored(title,"green"),
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
        "Question": {"mark_color": split_color("green"), "brackets_color": split_color("yellow")},
        "List": {"selection_color": split_color("light_blue"), "selection_cursor": ">"},
    }
    return inquirer.themes.load_theme_from_dict(theme_dict)

theme = split_theme()