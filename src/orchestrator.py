import logging
import time

from dotenv import load_dotenv
import os

from src.remediation.github_remediation import GithubRemediation
from src.github_client import GitHubClient
from src.scanner.scanner import GithubScanner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("ORCHESTRATOR")


def orchestrate():
    github_token = os.getenv('GITHUB_TOKEN')
    github_client = GitHubClient(github_token)

    # Run scanner
    scanner = GithubScanner(github_client)
    scanner_results = scanner.scan()

    # Run remediation
    remediation = GithubRemediation(github_client, scanner_results)
    remediation.remediate()


if __name__ == "__main__":
    load_dotenv()

    start_time = time.time()
    orchestrate()
    duration_time = time.time() - start_time
    logger.info(f"Orchestrator duration time: {duration_time:.2f} seconds")
