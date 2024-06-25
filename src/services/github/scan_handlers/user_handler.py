from src.scanner import logger
from src.services.github.github_client import GitHubClient


class UserHandler:
    def __init__(self, github_client: GitHubClient):
        self.user = github_client.get_user()

    def check_require_2fa(self):
        return not self.user.two_factor_authentication

    def run(self, configurations):
        logger.info("Scanning user")

        results = []
        for config in configurations:
            try:
                if "check_function" in config and not config.get("check_function"):
                    continue  # should be handled with jsonschema

                check_function = getattr(self, config['check_function'])
                is_misconfigured = check_function()
                results.append({
                    "name": config["name"],
                    "description": config["description"],
                    "is_misconfigured": is_misconfigured
                })
            except Exception as e:
                logger.warning(f"Error checking configuration for user: {e}")
                continue

        return results
