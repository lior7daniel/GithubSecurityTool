from github import GithubException

from src.scanner.common import extract_configurations_file, GITHUB_REPOSITORY_CONFIGURATION_PATH, logger
from src.github_client import GitHubClient


class RepositoryHandler:
    def __init__(self, github_client: GitHubClient, repo_name: str):
        self.github_client = github_client
        self.configurations = extract_configurations_file(GITHUB_REPOSITORY_CONFIGURATION_PATH)
        self.repo_name = repo_name

    def check_main_branch_protection(self, repo):
        branch_protection = True
        try:
            main_branch_name = self.github_client.get_main_branch_name(repo.full_name)
            branch_protection = repo.get_branch(main_branch_name).protected
        except GithubException:
            logger.warning(f"The repository '{repo.name}' has not initiated its main branch yet.")
        return not branch_protection

    @staticmethod
    def check_dependabot_alerts(repo):
        try:
            dependabot_alerts_status = repo.get_vulnerability_alert()
            return not dependabot_alerts_status
        except GithubException:
            logger.warning(f"Dependabot alerts are not available for {repo.name}")
            return True

    @staticmethod
    def check_repository_public_access(repo):
        return not repo.private

    @staticmethod
    def check_repository_access(repo):
        try:
            collaborators = repo.get_collaborators()
            for collaborator in collaborators:
                if not collaborator.permissions.admin and not collaborator.permissions.push:
                    return True
            return False
        except GithubException as e:
            logger.warning(f"Failed to retrieve collaborators for {repo.name}: {e}")
            return True

    @staticmethod
    def check_encrypted_secrets(repo):
        try:
            secrets = repo.get_secrets()
            for secret in secrets:
                if not secret.encrypted_value:
                    return True
            return False
        except GithubException as e:
            logger.warning(f"Failed to retrieve secrets for {repo.name}: {e}")
            return True

    def run(self):
        logger.info("Scanning repositories")

        if self.repo_name:
            results = self.scan_repo()
        else:
            results = self.scan_repos()

        return results

    def scan_repo(self):
        results = []
        repo = self.github_client.get_repository(self.repo_name)
        repo_results = self.scan_repo_configurations(repo)

        results.append({
            "repository": repo.name,
            "results": repo_results
        })

        return results

    def scan_repos(self):
        results = []
        repos = self.github_client.list_repositories()
        for repo in repos:
            repo_results = self.scan_repo_configurations(repo)

            results.append({
                "repository": repo.name,
                "results": repo_results
            })

        return results

    def scan_repo_configurations(self, repo):
        repo_results = []
        for config_name, config in self.configurations.items():
            try:
                if "check_function" in config and not config.get("check_function"):
                    continue

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

        return repo_results
