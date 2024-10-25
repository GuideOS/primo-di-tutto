import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
application_path = os.path.dirname(script_dir)

# JSON-Datei laden (oder die Daten als String verwenden)
with open(f"{application_path}/tabs/gaming.json", "r") as f:
    games = json.load(f)

# Zugriff auf die Daten
for game in games:
    print(game["Name"], game["Package"])
