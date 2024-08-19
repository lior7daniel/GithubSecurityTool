from github import Github


class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.client = Github(token)

    def get_repository(self, repo_name):
        return self.client.get_repo(repo_name)

    def list_repositories(self):
        return self.client.get_user().get_repos()

    def get_user(self):
        return self.client.get_user()

    def get_main_branch_name(self, repo_name):
        repo = self.get_repository(repo_name)
        main_branch = repo.default_branch
        return main_branch
