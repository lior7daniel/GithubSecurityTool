import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from dotenv import load_dotenv
from src.common import ServiceType, extract_configurations_file, GITHUB_USER_CONFIGURATION_PATH, \
    GITHUB_REPOSITORY_CONFIGURATION_PATH
from src.scanner import BaseScanner, logger
from src.services.github.github_client import GitHubClient
from src.services.github.scan_handlers.repository_handler import RepositoryHandler
from src.services.github.scan_handlers.user_handler import UserHandler


class GithubScanner(BaseScanner):
    def __init__(self, github_client: GitHubClient):
        super().__init__(service=ServiceType.GITHUB, client=github_client)
        self.user_handler = UserHandler(github_client)
        self.repository_handler = RepositoryHandler(github_client)
        self.configurations: Dict[str, Dict[str, Dict[str, str]]] = {
            "user": extract_configurations_file(GITHUB_USER_CONFIGURATION_PATH),
            "repository": extract_configurations_file(GITHUB_REPOSITORY_CONFIGURATION_PATH)
        }

    def scan(self):
        with ThreadPoolExecutor() as executor:
            # TODO: Run all the scan_handlers dynamically
            user_future = executor.submit(self.user_handler.run, self.configurations["user"])
            repository_future = executor.submit(self.repository_handler.run, self.configurations["repository"])

            results = {
                "metadata": {
                    "service": self.service.value,
                },
                "user_results": user_future.result(),
                "repository_results": repository_future.result()
            }

        self.results = results
        self.save_scan_result_file()

        return results


if __name__ == "__main__":
    start_time = time.time()

    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    github_client = GitHubClient(github_token)

    scanner = GithubScanner(github_client)
    scanner.scan()

    duration_time = time.time() - start_time

    logger.info(f"GithubScanner duration time: {duration_time:.2f} seconds")
