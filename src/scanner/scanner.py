import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

from src.github_client import GitHubClient
from src.scanner.common import logger, save_scan_result_file
from src.scanner.scan_handlers.repository_handler import RepositoryScannerHandler
from src.scanner.scan_handlers.user_handler import UserScannerHandler


class Scanner:
    def __init__(self, client: GitHubClient, repo_name: str):
        self.client = client
        self.results = {}
        self.repo_full_name = client.get_user().login + "/" + repo_name if repo_name else None

    def scan(self):
        logger.info("*** START SCANNING ***")

        user_handler = UserScannerHandler(self.client)
        repo_handler = RepositoryScannerHandler(self.client, self.repo_full_name)

        with ThreadPoolExecutor() as executor:
            user_scanner = executor.submit(user_handler.run)
            repo_scanner = executor.submit(repo_handler.run)

            results = {
                "metadata": {
                    "service": "github",
                },
                "user_results": user_scanner.result(),
                "repository_results": repo_scanner.result()
            }

        self.results = results
        save_scan_result_file(results)

        return results


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Run the scanner component.")
    parser.add_argument("--repo-name", help="A specific repository to scan.")
    args = parser.parse_args()

    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    client = GitHubClient(github_token)

    scanner = Scanner(client, args.repo_name)
    scanner.scan()

    duration_time = time.time() - start_time

    logger.info(f"GithubScanner duration time: {duration_time:.2f} seconds")
