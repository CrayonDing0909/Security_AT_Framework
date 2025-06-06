import json
from pathlib import Path


def load_json_data(file_path):
    with open(Path(file_path), "r", encoding="utf-8") as f:
        return json.load(f)
