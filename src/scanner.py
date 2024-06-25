import json
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

from src.common import ServiceType, ROOT_DIR, BaseClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s")
logger = logging.getLogger("SCANNER")


class BaseScanner(ABC):
    def __init__(self, service: ServiceType, client: BaseClient):
        self.service = service
        self.client = client
        self.results = {}

    @abstractmethod
    def scan(self):
        pass

    @staticmethod
    def extract_configurations_file(path):
        with open(path, 'r') as f:
            configurations = json.load(f)

        return configurations

    def save_scan_result_file(self):
        timestamp = datetime.utcnow().strftime('%Y-%m-%d--%H:%M:%S')

        directory = f'{ROOT_DIR}/results/{self.service.value}'
        filename = f'{directory}/scan_results_{timestamp}.json'
        os.makedirs(directory, exist_ok=True)

        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)

        return filename
