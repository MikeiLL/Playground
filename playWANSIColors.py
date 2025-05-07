#!/usr/bin/python3

"""
Some ANSI color experiments

Stands for "American National Standards Institute"
ANSI escape codes are a standard for in-band signaling to control cursor location, color, font styling, and other options on text terminals.
ANSI escape codes are used to format text in a terminal, allowing for color changes, text styles (like bold or underline), and cursor movements.
Resource: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
"""

print("\u001b[31mRed is 31m\u001b[0m")  # Red text

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

for color_name, color_code in ANSI_COLORS.items():
    print(f"{color_code}This is {color_name} text{RESET}")

# 256 COLORS
# 256 colors are represented by numbers from 0 to 255.
# The first 16 colors are the standard ANSI colors.
# The next 216 colors are a 6x6x6 RGB cube, which gives you a range of colors.
# The last 40 colors are grayscale colors.
for i in range(256):
    print(f"\u001b[38;5;{i}mColor {i}\u001b[0m", end=' ')
    if (i + 1) % 16 == 0:
        print()  # New line every 16 colors
# 24-bit RGB colors
# 24-bit RGB colors are represented by three numbers, each ranging from 0 to 255.
# This allows for over 16 million colors.
# The format is \u001b[38;2;<r>;<g>;<b>m where <r>, <g>, and <b> are the red, green, and blue values respectively.
for r in range(0, 256, 51):
    for g in range(0, 256, 51):
        for b in range(0, 256, 51):
            print(f"\u001b[38;2;{r};{g};{b}mColor ({r}, {g}, {b})\u001b[0m", end=' ')
        print()  # New line after each row
# 256 colors with background
for i in range(256):
    print(f"\u001b[48;5;{i}mColor {i}\u001b[0m", end=' ')
    if (i + 1) % 16 == 0:
        print()  # New line every 16 colors
# 24-bit RGB colors with background
for r in range(0, 256, 51):
    for g in range(0, 256, 51):
        for b in range(0, 256, 51):
            print(f"\u001b[48;2;{r};{g};{b}mColor ({r}, {g}, {b})\u001b[0m", end=' ')
        print()  # New line after each row
