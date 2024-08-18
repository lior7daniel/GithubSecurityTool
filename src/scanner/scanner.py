import argparse
import json
import os
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from dotenv import load_dotenv

from src.scanner.common import SCANNER_DIR, BaseClient, ServiceType, logger
from src.github_client import GitHubClient
from src.scanner.scan_handlers.repository_handler import RepositoryHandler
from src.scanner.scan_handlers.user_handler import UserHandler


class BaseScanner(ABC):
    def __init__(self, service: ServiceType, client: BaseClient):
        self.service = service
        self.client = client
        self.results = {}

    @abstractmethod
    def scan(self):
        pass

    def save_scan_result_file(self):
        timestamp = datetime.utcnow().strftime('%Y-%m-%d--%H:%M:%S')

        directory = f'{SCANNER_DIR}/results/{self.service.value}'
        filename = f'{directory}/{timestamp}.json'
        os.makedirs(directory, exist_ok=True)

        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)

        logger.info(f"Output file created successfully - file name: {filename}")

        return filename


class GithubScanner(BaseScanner):
    def __init__(self, client: GitHubClient, repo_name: str):
        super().__init__(service=ServiceType.GITHUB, client=client)
        self.repo_name = repo_name

    def scan(self):
        with ThreadPoolExecutor() as executor:
            user_scanner = executor.submit(UserHandler(github_client).run)
            repo_scanner = executor.submit(RepositoryHandler(github_client, self.repo_name).run)

            results = {
                "metadata": {
                    "service": self.service.value,
                },
                "user_results": user_scanner.result(),
                "repository_results": repo_scanner.result()
            }

        self.results = results
        self.save_scan_result_file()

        return results


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Run the scanner component.")
    parser.add_argument("--repo-name", help="A specific repository to scan.")
    args = parser.parse_args()

    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    github_client = GitHubClient(github_token)
    repo_prefix = github_client.get_user().login

    scanner = GithubScanner(github_client, repo_prefix + "/" + args.repo_name)
    scanner.scan()

    duration_time = time.time() - start_time

    logger.info(f"GithubScanner duration time: {duration_time:.2f} seconds")
