import sys, os

def clear():
    os.system("clear")

def rgbBg(c):
    if "#" in c:
        c = hex_to_rgb(c)
    return f"\033[48;2;{c[0]};{c[1]};{c[2]}m"


def rgbFg(c):
    if "#" in c:
        c = hex_to_rgb(c)
    return f"\033[38;2;{c[0]};{c[1]};{c[2]}m"


def clear_colors():
    return "\033[0m"
    
def rgb_to_hex(r, g, b):
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_color

def reset_cursor():
    sys.stdout.write("\033[u")

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)