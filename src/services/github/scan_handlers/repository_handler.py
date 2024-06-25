from typing import Dict

from github import GithubException

from src.scanner import logger
from src.services.github.github_client import GitHubClient


class RepositoryHandler:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client
        self.repos = github_client.list_repositories()

    def check_branch_protection(self, repo):
        branch_protection = True
        try:
            main_branch_name = self.github_client.get_main_branch_name(repo.full_name)
            branch_protection = repo.get_branch(main_branch_name).protected
        except GithubException as e:
            logger.warning(f"The repository '{repo.name}' has not initiated its main branch yet.")
        return not branch_protection

    @staticmethod
    def check_repository_public_access(repo):
        return not repo.private

    def run(self, configurations: Dict[str, Dict[str, str]]):
        logger.info("Scanning repositories")
        repos = self.repos

        results = []
        for repo in repos:
            repo_results = []
            for config_name, config in configurations.items():
                try:
                    if "check_function" in config and not config.get("check_function"):
                        continue    # information about the missing function should be handled in other test

                    check_function = getattr(self, config["check_function"])
                    is_misconfigured = check_function(repo)
                    repo_results.append({
                        "name": config_name,
                        "description": config["description"],
                        "is_misconfigured": is_misconfigured
                    })
                except Exception as e:
                    logger.warning(f"Failed checking {config_name=} for repository {repo.name}: {e}")
                    continue

            results.append({
                "repository": repo.name,
                "results": repo_results
            })

        return results
