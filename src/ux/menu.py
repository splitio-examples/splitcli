import inquirer

from ux.text import colored, get_color

def output_message(message, option="Continue"):
    print(colored(message,"split_yellow"))

def option_unavailable():
    output_message("Option unavailable", "Back")

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