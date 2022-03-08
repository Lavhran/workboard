import webbrowser
import os

def open_url(url: str, event=None) -> None:
    webbrowser.open(url)

def open_file(path: str, event=None) -> None:
    os.startfile(path)
