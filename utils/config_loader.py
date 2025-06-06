# utils/config_loader.py
import json
import os


def get_config(env=None):
    env = env or os.getenv("TEST_ENV", "dev")
    with open(f"config/{env}.json", "r", encoding="utf-8") as f:
        return json.load(f)
