import json
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s")
logger = logging.getLogger("REMEDIATION")

REMEDIATION_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(REMEDIATION_DIR)
SCANNER_RESULTS_DIR = f"{ROOT_DIR}/scanner/results"


def load_scanner_results(scanner_results_path: str = None):
    if scanner_results_path:
        if not os.path.exists(scanner_results_path):
            raise FileNotFoundError(f"Scanner results file '{scanner_results_path}' not found.")
        with open(scanner_results_path, 'r') as f:
            return json.load(f)
    else:
        result_files = [f for f in os.listdir(SCANNER_RESULTS_DIR) if f.endswith('.json')]
        if not result_files:
            raise FileNotFoundError("No scan results found in the results directory.")
        latest_scan_results = max(result_files)
        with open(os.path.join(SCANNER_RESULTS_DIR, latest_scan_results), 'r') as f:
            return json.load(f)
