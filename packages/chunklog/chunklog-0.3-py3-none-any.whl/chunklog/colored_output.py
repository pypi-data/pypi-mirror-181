import difflib
from chunklog.console import console
from rich.text import Text

"""
With rich, but not trivial to switch to as get_edits_string concatenates strings and rich makes their own Text object
red = lambda text: (Text.assemble(text, "red"))
green = lambda text: (Text.assemble(text, "green"))
blue = lambda text: (Text.assemble(text, "blue"))
white = lambda text: (Text.assemble(text, "white"))
"""

red = lambda text: f"\033[38;2;255;0;0m{text}\033[38;2;255;255;255m"
green = lambda text: f"\033[38;2;0;255;0m{text}\033[38;2;255;255;255m"
blue = lambda text: f"\033[38;2;0;0;255m{text}\033[38;2;255;255;255m"
white = lambda text: f"\033[38;2;255;255;255m{text}\033[38;2;255;255;255m"


def get_edits_string(old, new):
    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal":
            result += white(old[code[1] : code[2]])
        elif code[0] == "delete":
            result += red(old[code[1] : code[2]])
        elif code[0] == "insert":
            result += green(new[code[3] : code[4]])
        elif code[0] == "replace":
            result += red(old[code[1] : code[2]]) + green(new[code[3] : code[4]])
    return result
