from ux.hex_color import match_256

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

foreground = standard_colors['bright_white']

# TODO: Dark / Light / Uncolored modes

def colored(text, color_name):
    color = get_color(color_name)
    return color + text + get_color(foreground)

def get_color(color_name):
    return split_colors.get(color_name, standard_colors.get(color_name, foreground))