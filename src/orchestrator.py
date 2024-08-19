import argparse
import logging
import time

from dotenv import load_dotenv
import os

from src.github_client import GitHubClient
from src.remediation.remediation import Remediation
from src.scanner.scanner import Scanner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("ORCHESTRATOR")


def orchestrate():
    token = os.getenv('GITHUB_TOKEN')
    client = GitHubClient(token)

    # Run scanner
    scanner = Scanner(client, args.repo_name)
    scanner_results = scanner.scan()

    # Run remediation
    remediation_user_interface = args.remediation_user_interface == "true"
    remediation = Remediation(client, scanner_results, remediation_user_interface)
    remediation.remediate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the scanner component.")
    parser.add_argument("--repo-name", help="A specific repository to scan.")
    parser.add_argument("--remediation-user-interface", default=False,
                        help="Set to 'true' to enable remediation user interface")
    args = parser.parse_args()

    load_dotenv()

    start_time = time.time()
    orchestrate()
    duration_time = time.time() - start_time
    logger.info(f"Orchestrator duration time: {duration_time:.2f} seconds")
