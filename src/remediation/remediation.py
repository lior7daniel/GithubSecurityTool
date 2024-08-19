import argparse
import os
import time

from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

from src.remediation.common import load_scanner_results, logger
from src.remediation.remediation_handlers.repository_handler import RepositoryRemediationHandler
from src.remediation.remediation_handlers.user_handler import UserRemediationHandler
from src.github_client import GitHubClient


class Remediation:
    def __init__(self, client: GitHubClient, scanner_results, remediation_user_interface):
        self.client = client
        self.scanner_results = scanner_results
        self.remediation_user_interface = remediation_user_interface

    def remediate(self):
        logger.info("*** START SCANNING ***")
        user_res = self.scanner_results.get("user_results", [])
        repos_res = self.scanner_results.get("repository_results", [])
        user_handler = UserRemediationHandler(self.client, user_res)
        repo_handler = RepositoryRemediationHandler(self.client, repos_res, self.remediation_user_interface)

        with ThreadPoolExecutor() as executor:
            executor.submit(user_handler.run)
            executor.submit(repo_handler.run)


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Run the remediation component based on scanner results.")
    parser.add_argument("--scanner-results-path", help="Path to the scanner results JSON file.")
    parser.add_argument("--remediation-user-interface", default=False,
                        help="Set to 'true' to enable remediation user interface")

    args = parser.parse_args()

    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    client = GitHubClient(github_token)

    remediation_user_interface = args.remediation_user_interface == "true"
    scanner_results = load_scanner_results(scanner_results_path=args.scanner_results_path)
    remediation = Remediation(client, scanner_results, remediation_user_interface)
    remediation.remediate()
