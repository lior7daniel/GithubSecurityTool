import os
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from src.common import ROOT_DIR, ServiceType, BaseClient
from src.scanner import BaseScanner, logger
from src.services.github.github_client import GitHubClient
from src.services.github.scan_handlers.repository_handler import RepositoryHandler
from src.services.github.scan_handlers.user_handler import UserHandler

GITHUB_CONFIGURATIONS = os.path.join(ROOT_DIR, 'services', 'github', 'configurations')
USER_CONFIGURATION_PATH = f"{GITHUB_CONFIGURATIONS}/user_configurations.json"
REPOSITORY_CONFIGURATION_PATH = f"{GITHUB_CONFIGURATIONS}/repository_configurations.json"
HANDLERS = os.path.join(ROOT_DIR, 'services', 'github', 'scan_handlers')


class GithubScanner(BaseScanner):
    def __init__(self, github_client: BaseClient):
        super().__init__(service=ServiceType.GITHUB, client=github_client)
        self.user_handler = UserHandler(github_client)
        self.repository_handler = RepositoryHandler(github_client)
        self.configurations = {
            "user": self.extract_configurations_file(USER_CONFIGURATION_PATH),
            "repository": self.extract_configurations_file(REPOSITORY_CONFIGURATION_PATH)
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
