#!/usr/bin/python3

"""
Some ANSI color experiments

Stands for "American National Standards Institute"
ANSI escape codes are a standard for in-band signaling to control cursor location, color, font styling, and other options on text terminals.
ANSI escape codes are used to format text in a terminal, allowing for color changes, text styles (like bold or underline), and cursor movements.
Resource: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
Resource: https://stackoverflow.com/a/33206814/2223106
"""

ANSI_COLORS = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "reset": "\u001b[0m"
}
# Foreground colors
COLORS = {
    "1xx": ANSI_COLORS["green"],
    "2xx": ANSI_COLORS["yellow"],
    "3xx": ANSI_COLORS["blue"],
    "4xx": ANSI_COLORS["magenta"],
    "5xx": ANSI_COLORS["red"],
    "Invalid": ANSI_COLORS["white"]
}
# Background colors
BG_COLORS = {
    "1xx": "\u001b[42m",
    "2xx": "\u001b[43m",
    "3xx": "\u001b[44m",
    "4xx": "\u001b[45m",
    "5xx": "\u001b[41m",
    "Invalid": "\u001b[47m"
}
# Styles
STYLES = {
    "bold": "\u001b[1m",
    "underline": "\u001b[4m",
    "blink": "\u001b[5m",
    "reverse": "\u001b[7m"
}
# Reset
RESET = "\u001b[0m"
# Example usage
""" print(f"{COLORS['1xx']}This is a 1xx status code message{RESET}")
print(f"{COLORS['2xx']}This is a 2xx status code message{RESET}")
 """

print("\n\u001b[1m8 basic colors\u001b[0m: \n\n")
for color_name, color_code in ANSI_COLORS.items():
    if color_name == "black":
        print(f"\u001b[47;30mThis is {color_name} text{RESET}")
    elif color_name == "blue":
        print(f"\u001b[47;34mThis is {color_name} text{RESET}")
    else:
      print(f"{color_code}This is {color_name} text{RESET}")


print("\n\u001b[35;42;4;1;mHere's one with bold underline and BG and FG\u001b[0m: \n")

# 256 COLORS
# 256 colors are represented by numbers from 0 to 255.
# The first 16 colors are the standard ANSI colors.
# The next 216 colors are a 6x6x6 RGB cube, which gives you a range of colors.
# The last 40 colors are grayscale colors.
print("\n\u001b[1m256 colors\u001b[0m: \n\n")
for i in range(256):
    print(f"\u001b[38;5;{i}mColor {i}\u001b[0m", end=' ')
    if (i + 1) % 16 == 0:
        print()  # New line every 16 colors
# 24-bit RGB colors
# 24-bit RGB colors are represented by three numbers, each ranging from 0 to 255.
# This allows for over 16 million colors.
# The format is \u001b[38;2;<r>;<g>;<b>m where <r>, <g>, and <b> are the red, green, and blue values respectively.
print("\n\u001b[1m24-bit RGB colors\u001b[0m: \n")
for r in range(0, 256, 51):
    for g in range(0, 256, 51):
        for b in range(0, 256, 51):
            print(f"\u001b[38;2;{r};{g};{b}mColor ({r}, {g}, {b})\u001b[0m", end=' ')
        print("\n")  # New line after each row

# 256 colors with background
print("\n\u001b[1m256 colors with background\u001b[0m: \n")
for i in range(256):
    print(f"\u001b[48;5;{i}mColor {i}\u001b[0m", end=' ')
    if (i + 1) % 16 == 0:
        print("\n")  # New line every 16 colors

# 24-bit RGB colors with background
print("\n\u001b[1m24-bit RGB colors with background\u001b[0m: \n")
for r in range(0, 256, 51):
    for g in range(0, 256, 51):
        for b in range(0, 256, 51):
            print(f"\u001b[48;2;{r};{g};{b}mColor ({r}, {g}, {b})\u001b[0m", end=' ')
        print("\n")  # New line after each row

print("\n\u001b[1mNow some stuff from the Wikipedia page thank you Thomas Dickey\u001b[0m: \n")
# print a list of the 256-color red/green/blue values used by xterm.
#
# reference:
# https://github.com/ThomasDickey/ncurses-snapshots/blob/master/test/xterm-16color.dat
# https://github.com/ThomasDickey/xterm-snapshots/blob/master/XTerm-col.ad
# https://github.com/ThomasDickey/xterm-snapshots/blob/master/256colres.pl

print("\n\u001b[1mColors 0-16 correspond to the ANSI and aixterm naming\u001b[0m\n\n")
for code in range(0, 16):
    if code > 8:
        level = 255
    elif code == 7:
        level = 229
    else:
        level = 205
    r = 127 if code == 8 else level if (code & 1) != 0 else 92 if code == 12 else 0
    g = 127 if code == 8 else level if (code & 2) != 0 else 92 if code == 12 else 0
    b = 127 if code == 8 else 238 if code == 4 else level if (code & 4) != 0 else 0
    print(f"{code:3d}: \u001b[48;2;{r};{g};{b}m        \u001b[0m   {r:02X} {g:02X} {b:02X}")

print("\n\u001b[1mColors 16-231 are a 6x6x6 color cube\u001b[0m\n\n")
for red in range(0, 6):
    for green in range(0, 6):
        for blue in range(0, 6):
            code = 16 + (red * 36) + (green * 6) + blue
            r = red   * 40 + 55 if red   != 0 else 0
            g = green * 40 + 55 if green != 0 else 0
            b = blue  * 40 + 55 if blue  != 0 else 0
            print(f"{code:3d}: \u001b[48;2;{r};{g};{b}m        \u001b[0m   {r:02X} {g:02X} {b:02X}")

print("\n\u001b[1mColors 232-255 are a grayscale ramp, intentionally leaving out black and white\u001b[0m\n\n")
code = 232
for gray in range(0, 24):
    level = gray * 10 + 8
    code = 232 + gray
    print(f"{code:3d}: \u001b[30;48;2;{level};{level};{level}m        \u001b[0m   {level:02X} {level:02X} {level:02X}")
