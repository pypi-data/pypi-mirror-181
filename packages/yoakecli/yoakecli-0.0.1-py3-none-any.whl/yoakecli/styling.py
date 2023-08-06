import os
from enum import Enum

os.system('')

class Text(Enum):
    BLACK = '\x1b[30m'
    RED = '\x1b[91m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    BLUE = '\x1b[94m'
    MAGENTA = '\x1b[95m'
    CYAN = '\x1b[96m'
    WHITE = '\x1b[37m'
    DEFAULT = '\x1b[39m'
    BOLD = '\x1b[1m'
    ITALIC = '\x1b[3m'
    UNDERSCORE = '\x1b[4m'
    STRIKETHROUGH = '\x1b[9m'

def erase_line():
    print(end='\x1b[2K')

def cursor_show():
    print(end='\x1b[?25h')

def cursor_hide():
    print(end='\x1b[?25l')

def cursor_up(line=1):
    print(end=f'\x1b[{line}A')

def erase_from_startline():
    print(end='\x1b[1K')

def erase_to_endline():
    print(end='\x1b[0K')

def erase_screen():
    print(end='\x1b[2J')

def erase_screen_from_cursor():
    print(end='\x1b[J')

def style_reset():
    print(end='\x1b[0m')

def print_style(text:str, *style, endchar='\n'):
    if len(style) == 0:
        style = (Text.DEFAULT,)
    style_str = ''.join(map(lambda x: str(x.value), style))
    start = text.find('\x1b[')
    end = text.rfind('\x1b[0m')
    if start >= 0 and end >= 0 and end > start:
        text = text[:start] + '\x1b[0m' + text[start:end + 4] + style_str + text[end + 4:]
    print(style_str + text + '\x1b[0m', end=endchar)

def string_style(text:str, *style):
    if len(style) == 0:
        style = (Text.DEFAULT,)
    style_str = ''.join(map(lambda x: str(x.value), style))
    start = text.find('\x1b[')
    end = text.rfind('\x1b[0m')
    if start >= 0 and end >= 0 and end > start:
        text = text[:start] + '\x1b[0m' + text[start:end + 4] + style_str + text[end + 4:]
    return style_str + text + '\x1b[0m'