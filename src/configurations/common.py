import json
import os

CONFIGURAION_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIGURATION_FILE = f"{CONFIGURAION_DIR}/user_configurations.json"
REPOSITORY_CONFIGURATION_FILE = f"{CONFIGURAION_DIR}/repository_configurations.json"


def extract_configurations_file(path):
    with open(path, 'r') as f:
        configurations = json.load(f)

    return configurations
