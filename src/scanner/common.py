import json
import logging
import os
from datetime import datetime
from typing import Dict, Any

SCANNER_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s")
logger = logging.getLogger("SCANNER")


def save_scan_result_file(results: Dict[str, Dict[Any, Any]]):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')

    directory = f"{SCANNER_DIR}/results"
    os.makedirs(directory, exist_ok=True)
    filename = f"{directory}/{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

    logger.info(f"Output file created successfully - file name: {filename}")

    return filename
