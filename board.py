import config as c
import json

try:
    with open(c.config["board"]["path"], "r") as f:
        workboard = json.load(f)
except:
    workboard = {}

def add(table: dict) -> None:
    workboard[table["title"]] = table
    save()

def remove(title: str) -> None:
    del workboard[title]
    save()

def update(table: dict, old_title: str) -> None:
    remove(old_title)
    add(table)

def save() -> None:
    with open(c.config["board"]["path"], "w") as f:
        json.dump(workboard, f, indent=3)
