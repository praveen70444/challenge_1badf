import json
import os

def load_input_json(input_folder="input"):
    input_path = os.path.join(input_folder, "challenge1b_input.json")
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)
