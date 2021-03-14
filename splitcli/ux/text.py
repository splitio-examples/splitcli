from splitcli.ux.hex_color import match_256
import re

def set_theme(is_dark=True):
    global is_dark_theme
    is_dark_theme = is_dark

def get_theme():
    return themes.get(is_dark_theme, None)

def colored(text, color_name):
    color = get_color(color_name)
    return color + text + get_color("foreground")

def get_color(color_name):
    theme = get_theme()
    if theme == None:
        return ""
    if color_name in theme:
        return get_color(theme[color_name])
    if color_name in split_colors:
        return split_colors[color_name]
    if color_name in standard_colors:
        return standard_colors[color_name]
    return theme["foreground"]

def inquirer_theme():
    return inquirer_themes.get(is_dark_theme, None)

def split_logo():
    logo = split_logo_plain
    logo = logo.replace("/", colored("/", "split_blue_dark"))
    logo = logo.replace(",", colored(",", "split_blue_light"))
    logo = logo.replace("@", colored("@", "foreground"))
    return logo

split_logo_plain = """
              /////
          /////////                                            @@@   @@    @@@
     ///////////                                               @@@   @@    @@@
 ///////////,,,,,                   @@@@@@    @@  @@@@@@@      @@@   @@  @@@@@@@
///////   ,,,,,,,,,,,              @@    @@   @@@@      @@@    @@@   @@    @@@
/////////     ,,,,,,,,,,,          @@@@@      @@          @@   @@@   @@    @@@
  ///////////      ,,,,,,,,            @@@@   @@          @@   @@@   @@    @@@
       ///////////  ,,,,,,,       @@@    @@@  @@@@      @@@    @@@   @@    @@@
           ////////,,,,,,,          @@@@@@    @@  @@@@@@@      @@@   @@    @@@
           ,,,,,///,,,                        @@
         ,,,,,,,,,                            @@
         ,,,,
"""

split_colors = {
    "split_black": match_256("333333"),
    "split_blue_dark": match_256("0470ca"),
    "split_blue_light": match_256("00c5fd"),
    "split_green": match_256("0be4b8"),
    "split_yellow": match_256("ffc825")
}

standard_colors = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "grey": "\u001b[90m",
    "bright_red": "\u001b[91m",
    "bright_green": "\u001b[92m",
    "bright_yellow": "\u001b[93m",
    "bright_blue": "\u001b[94m",
    "bright_magenta": "\u001b[95m",
    "bright_cyan": "\u001b[96m",
    "bright_white": "\u001b[97m",
    "reset": "\u001b[0",
}

is_dark_theme = True
themes = {
    True: {
        "foreground": "bright_white",
    },
    False: {
        "foreground": "split_black",
    }
}

inquirer_themes = {
    True: {
        "Question": {"mark_color": get_color("split_yellow"), "brackets_color": get_color("split_green")},
        "List": {"selection_color": get_color("split_blue_light"), "selection_cursor": ">"},
    },
    False: {
        "Question": {"mark_color": get_color("split_yellow"), "brackets_color": get_color("split_green")},
        "List": {"selection_color": get_color("split_blue_dark"), "selection_cursor": ">"},
    }
}