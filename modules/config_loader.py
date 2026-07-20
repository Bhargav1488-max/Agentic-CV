import yaml
import os
from dotenv import load_dotenv

load_dotenv()

def load_config(config_path="config.yaml"):
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

CONFIG = load_config()

def get_providers():
    return CONFIG.get("providers", {})

def get_languages():
    return CONFIG.get("languages", ["English", "French"])

def get_templates():
    return CONFIG.get("cv_templates", ["Modern", "Classic", "ATS-Safe"])
