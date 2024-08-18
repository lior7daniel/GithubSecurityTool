import json
import logging
import os
from enum import Enum
from abc import ABC

SCANNER_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_CONFIGURATIONS = os.path.join(SCANNER_DIR, 'configurations')
GITHUB_USER_CONFIGURATION_PATH = f"{GITHUB_CONFIGURATIONS}/user_configurations.json"
GITHUB_REPOSITORY_CONFIGURATION_PATH = f"{GITHUB_CONFIGURATIONS}/repository_configurations.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s")
logger = logging.getLogger("SCANNER")


class ServiceType(Enum):
    GITHUB = "github"


def extract_configurations_file(path):
    with open(path, 'r') as f:
        configurations = json.load(f)

    return configurations


class BaseClient(ABC):
    def __init__(self, token):
        self.token = token
