from src.configurations.common import extract_configurations_file, USER_CONFIGURATION_FILE
from src.github_client import GitHubClient
from src.remediation.common import logger


class UserRemediationHandler:
    def __init__(self, client: GitHubClient, user_results):
        self.client = client
        self.user = client.get_user()
        self.configurations = extract_configurations_file(USER_CONFIGURATION_FILE)
        self.user_results = user_results

    @staticmethod
    def fix_require_2fa():
        pass
    
    def run(self, user_results):
        logger.info("Remediate User")

        for result in user_results:
            if result["is_misconfigured"]:
                config_name = result["name"]
                config = self.configurations["user"][config_name]
                if "fix_function" in config and not config.get("fix_function"):
                    continue
                try:
                    fix_function = getattr(self, config["fix_function"])
                    fix_function(self.user)
                except Exception as e:
                    logger.warning(f"Failed to remediate {config_name=} for {self.user.name=} due to {e}")
                    continue
