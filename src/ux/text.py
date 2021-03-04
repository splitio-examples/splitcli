from ux.hex_color import best_match

def colored(text, color_name):
    color = split_color(color_name)
    return color + text + split_color("white")

def split_color(color_name):
    return split_colors.get(color_name, color_name)

split_colors = {
    "white": best_match("ffffff"),
    "black": best_match("333333"),
    "dark_blue": best_match("0470ca"),
    "light_blue": best_match("00c5fd"),
    "green": best_match("0be4b8"),
    "yellow": best_match("ffc825")
}