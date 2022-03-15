import json

CONFIGFILE = "config/config.json"

def save():
    with open(CONFIGFILE, "w") as f:
        json.dump(config, f, indent=3)

try:
    with open(CONFIGFILE, "r") as f:
        config = json.load(f)
except:
    config = {
        'font': {
            'title': ['Helvetica', 14],
            'default': ['Arial', 11]
        },
        'board': {
            'groups': [
                "Backlog",
                "Work in progress",
                "Done"
            ],
            'path': "board.json"
        },
        'view': {
            'maxlinklength': 40,
            'mode': "break",
            'labeled': [
                "URL",
                "FILE"
            ]
        }
    }
    save()

