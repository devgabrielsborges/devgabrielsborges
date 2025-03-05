import re
from github import Github


class Repository:
    def __init__(
        self, username: str,
        token: str,
        oculted_repos: list[str],
        working_on_section: str,
        readme_path="README.md"
    ):
        self.username = username
        self.oculted_repos = oculted_repos
        self.user = Github(token).get_user(username)
        self.repos = self.get_repos()
        self.active_repos = []
        self.readme_path = readme_path
        self.readme = self.get_readme(self.readme_path)
        self.working_on_section = working_on_section

    def get_repos(self) -> list:
        try:
            return list(self.user.get_repos(sort="updated"))
        except Exception as e:
            raise Exception(f"Repo fetching exception: {e}")

    def populate_active_repos(self):
        for repo in self.repos:
            if not repo.fork and repo.name not in self.oculted_repos:
                self.active_repos.append(repo)
            if len(self.active_repos) >= 3:
                break

    def get_readme(self, path):
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"# Hello, I'm {self.username}\n\n"

    def append_working_section(self):
        self.populate_active_repos()
        
        for repo in self.active_repos:
            description = repo.description or "No description available"
            self.working_on_section += f"- [{repo.name}]({repo.html_url}) - {description}\n"

    def update_readme(self, pattern: str):
        content = self.readme
        working_on_section = self.working_on_section

        if re.search(pattern, content):
            updated_content = re.sub(pattern, working_on_section, content)
        else:
            if "##" in content:
                position = content.find("##")
                updated_content = content[:position] + working_on_section + content[position:]
            else:
                updated_content = content + "\n" + working_on_section

        with open(self.readme_path, "w") as f:
            f.write(updated_content)
