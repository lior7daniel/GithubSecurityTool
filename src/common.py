import json
import os
from enum import Enum
from abc import ABC

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_CONFIGURATIONS = os.path.join(ROOT_DIR, 'services', 'github', 'configurations')
GITHUB_USER_CONFIGURATION_PATH = f"{GITHUB_CONFIGURATIONS}/user_configurations.json"
GITHUB_REPOSITORY_CONFIGURATION_PATH = f"{GITHUB_CONFIGURATIONS}/repository_configurations.json"


class ServiceType(Enum):
    GITHUB = "github"


def extract_configurations_file(path):
    with open(path, 'r') as f:
        configurations = json.load(f)

    return configurations


class BaseClient(ABC):
    def __init__(self, token):
        self.token = token

# class BaseHandler(ABC):
#     def __init__(self, client):
#         self.client = client
#
#     @abstractmethod
#     def run(self):
#         pass
