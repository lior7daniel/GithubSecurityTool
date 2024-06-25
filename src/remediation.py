import json
import logging
import os
from abc import ABC, abstractmethod

from src.common import ROOT_DIR, ServiceType

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s")
logger = logging.getLogger("REMEDIATION")


class BaseRemediation(ABC):
    def __init__(self, scanner_results):
        self.scanner_results = scanner_results

    @abstractmethod
    def remediate(self):
        pass

    @staticmethod
    def load_scanner_results(service_type: ServiceType, scanner_results_path: str = None):
        if scanner_results_path:
            with open(scanner_results_path, 'r') as f:
                return json.load(f)
        else:
            service = ""
            if service_type == ServiceType.GITHUB:
                service = "github"

            results_dir = os.path.join(ROOT_DIR, 'results', service)
            result_files = [f for f in os.listdir(results_dir) if f.startswith('scan_results_') and f.endswith('.json')]
            if not result_files:
                raise FileNotFoundError("No scan results found in the results directory.")
            latest_scan_results = max(result_files)
            with open(os.path.join(results_dir, latest_scan_results), 'r') as f:
                return json.load(f)
