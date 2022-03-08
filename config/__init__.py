import json

CONFIGFILE = "config/config.json"

def save():
    with open(CONFIGFILE, "w") as f:
        json.dump(config, f, indent=3)

try:
    with open(CONFIGFILE, "r") as f:
        config = json.load(f)
except:
    config = {}
    config["font"] = {
        "title": ["Helvetica", 14],
        "default": ["Arial", 11]}
    config["board"] = {
        "groups": ["Backlog", "Work in progress", "Done"],
        "path": "board.json"}
    save()

