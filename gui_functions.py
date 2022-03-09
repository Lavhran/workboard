import config as c
import webbrowser
import os

def open_url(url: str, event=None) -> None:
    webbrowser.open(url)

def open_file(path: str, event=None) -> None:
    os.startfile(path)

# text
def fix_text(text: str) -> str:
    length = c.config["view"]["maxlinklength"]

    if len(text) > length:
        if c.config["view"]["mode"] == "dot":
            text = dot_text(text, length)

        elif c.config["view"]["mode"] == "break":
            text = break_text(text, length)
    else:
        pass

    return text

def dot_text(text: str, length: int) -> str:
    return text[:length-3]+"..."

def break_text(text: str, length: int) -> str:
    text = list(text)
    for i in range(len(text)//length, 0, -1):
        text.insert(i*length, "\n")
    return "".join(text)
