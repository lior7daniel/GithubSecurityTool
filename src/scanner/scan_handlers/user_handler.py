from src.configurations.common import extract_configurations_file, USER_CONFIGURATION_FILE
from src.github_client import GitHubClient
from src.scanner.common import logger


class UserScannerHandler:
    def __init__(self, client: GitHubClient):
        self.user = client.get_user()
        self.configurations = extract_configurations_file(USER_CONFIGURATION_FILE)

    def check_require_2fa(self):
        return not self.user.two_factor_authentication

    def run(self):
        logger.info("Scanning user")

        results = []
        for config_name, config in self.configurations.items():
            try:
                if "check_function" in config and not config.get("check_function"):
                    continue

                check_function = getattr(self, config['check_function'])
                is_misconfigured = check_function()
                results.append({
                    "name": config_name,
                    "description": config["description"],
                    "is_misconfigured": is_misconfigured
                })
            except Exception as e:
                logger.warning(f"Failed checking {config_name=} for {self.user.name}: {e}")
                continue

        return results
