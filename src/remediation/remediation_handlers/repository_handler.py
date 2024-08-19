from src.configurations.common import extract_configurations_file, REPOSITORY_CONFIGURATION_FILE
from src.github_client import GitHubClient
from src.remediation.common import logger


class RepositoryRemediationHandler:
    def __init__(self, client: GitHubClient, repos_res, remediation_user_interface: bool = False):
        self.client = client
        self.repos_res = repos_res
        self.remediation_user_interface = remediation_user_interface
        self.configurations = extract_configurations_file(REPOSITORY_CONFIGURATION_FILE)
        self.remediation_user_interface = remediation_user_interface

    @staticmethod
    def ask_user_confirmation(message):
        while True:
            user_input = input(message + " (y/n): ").strip().lower()
            if user_input in ['y', 'n']:
                return user_input == 'y'
            print("Invalid input, please enter 'y' or 'n'.")

    def fix_main_branch_protection(self, repo):
        try:
            if self.remediation_user_interface:
                if not self.ask_user_confirmation(f"Do you want to enable branch protection for {repo.name}? (y/n): "):
                    logger.info(f"Skipping branch protection for {repo.name}")
                    return

            main_branch_name = self.client.get_main_branch_name(repo.full_name)
            branch = repo.get_branch(main_branch_name)

            branch.edit_protection(
                dismiss_stale_reviews=True,
                enforce_admins=True,
                require_code_owner_reviews=True,
                required_approving_review_count=1,
                lock_branch=True,
            )
            logger.info(f"Enabled branch protection for {repo.name}")
        except Exception as e:
            logger.warning(f"Failed to enable branch protection for {repo.name}: {e}")

    def fix_repository_public_access(self, repo):
        try:
            if self.remediation_user_interface:
                if not self.ask_user_confirmation(f"Do you want to disable public access for {repo.name}? (y/n): "):
                    logger.info(f"Skipping public access fix for {repo.name}")
                    return

            repo.edit(private=True)
            logger.info(f"Enabled private access for {repo.name}")
        except Exception as e:
            logger.warning(f"Failed to disable public access for {repo.name}: {e}")

    def fix_dependabot_alerts(self, repo):
        try:
            if self.remediation_user_interface:
                if not self.ask_user_confirmation(f"Do you want to enable Dependabot alerts for {repo.name}? (y/n): "):
                    logger.info(f"Skipping Dependabot alerts for {repo.name}")
                    return

            repo.enable_vulnerability_alert()
            logger.info(f"Enabled Dependabot alerts for {repo.name}")
        except Exception as e:
            logger.warning(f"Failed to enable Dependabot alerts for {repo.name}: {e}")

    def fix_repository_access(self, repo):
        try:
            if self.remediation_user_interface:
                if not self.ask_user_confirmation(
                        f"Do you want to restrict repository access for {repo.name}? (y/n): "):
                    logger.info(f"Skipping repository access restriction for {repo.name}")
                    return

            collaborators = repo.get_collaborators()
            for collaborator in collaborators:
                if not repo.organization.two_factor_requirement_enabled:
                    logger.info(f"Ensuring repository access restrictions for {repo.name}")
                    if collaborator.permissions.push or collaborator.permissions.admin:
                        logger.info(f"Restricting access for collaborator {collaborator.login}")
                        repo.remove_from_collaborators(collaborator)
                    else:
                        logger.info(f"Collaborator {collaborator.login} has limited access.")
        except Exception as e:
            logger.warning(f"Failed to restrict repository access for {repo.name}: {e}")

    def run(self):
        logger.info("Remediate Repositories")

        repo_prefix = self.client.get_user().login + "/"
        for repo_res in self.repos_res:
            repo_name = repo_prefix + repo_res["repository"]
            repo = self.client.get_repository(repo_name)
            for res in repo_res["results"]:
                if res['is_misconfigured']:
                    config_name = res["name"]
                    config = self.configurations[config_name]
                    if "fix_function" in config and not config.get("fix_function"):
                        continue
                    try:
                        fix_function = getattr(self, config["fix_function"])
                        fix_function(repo)
                    except Exception as e:
                        logger.warning(f"Failed to remediate {config_name=} for {repo.name=} due to {e}")
                        continue
