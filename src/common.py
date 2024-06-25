import os
from enum import Enum
from abc import ABC, abstractmethod

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class ServiceType(Enum):
    GITHUB = "github"


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
