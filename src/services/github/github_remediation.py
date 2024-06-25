import argparse
import json
import os
import time

from dotenv import load_dotenv

from src.common import extract_configurations_file, GITHUB_USER_CONFIGURATION_PATH, \
    GITHUB_REPOSITORY_CONFIGURATION_PATH, ROOT_DIR, ServiceType
from src.remediation import BaseRemediation, logger
from src.services.github.github_client import GitHubClient


class GithubRemediation(BaseRemediation):
    def __init__(self, github_client: GitHubClient, scanner_results):
        super().__init__(scanner_results)
        self.github_client = github_client
        self.configurations = {
            "user": extract_configurations_file(GITHUB_USER_CONFIGURATION_PATH),
            "repository": extract_configurations_file(GITHUB_REPOSITORY_CONFIGURATION_PATH)
        }

    def fix_require_2fa(self, user):
        pass

    @staticmethod
    def fix_repository_public_access(repo):
        repo.edit(private=True)

    def fix_branch_protection(self, repo):
        main_branch_name = self.github_client.get_main_branch_name(repo.full_name)
        branch = repo.get_branch(main_branch_name)
        branch.edit_protection(
            dismiss_stale_reviews=True,
            enforce_admins=True,
        )

    def remediate_user(self, user_results):
        user = self.github_client.get_user()
        for result in user_results:
            if result["is_misconfigured"]:
                config_name = result["name"]
                config = self.configurations["user"][config_name]
                if "fix_function" in config and not config.get("fix_function"):
                    continue  # should be handled with jsonschema
                try:
                    fix_function = getattr(self, config["fix_function"])
                    fix_function(user)
                except Exception as e:
                    logger.warning(f"Failed to remediate {config_name=} for {user.name=} due to {e}")
                    continue

    def remediate_repositories(self, repository_results):
        repo_prefix = self.github_client.get_user().login + "/"
        for repo_result in repository_results:
            repo_name = repo_prefix + repo_result["repository"]
            repo = self.github_client.get_repository(repo_name)
            for result in repo_result["results"]:
                if result['is_misconfigured']:
                    config_name = result["name"]
                    config = self.configurations["repository"][config_name]
                    if "fix_function" in config and not config.get("fix_function"):
                        continue  # should be handled with jsonschema
                    try:
                        fix_function = getattr(self, config["fix_function"])
                        fix_function(repo)
                    except Exception as e:
                        logger.warning(f"Failed to remediate {config_name=} for {repo.name=} due to {e}")
                        continue

    def remediate(self):
        user_results = self.scanner_results.get("user_results", [])
        repository_results = self.scanner_results.get("repository_results", [])

        self.remediate_user(user_results)
        self.remediate_repositories(repository_results)


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Run the remediation component based on scanner results.")
    parser.add_argument("--service-type", required=True, choices=[s.value for s in ServiceType], help="Service type to load results from.")
    parser.add_argument("--scanner-results-path", help="Path to the scanner results JSON file.")
    args = parser.parse_args()

    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    github_client = GitHubClient(github_token)

    scanner_results = BaseRemediation.load_scanner_results(service_type=args.service_type, scanner_results_path=args.scanner_results_path)
    remediation = GithubRemediation(github_client, scanner_results)
    remediation.remediate()
