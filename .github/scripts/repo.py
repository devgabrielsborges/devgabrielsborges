import re
from github import Github
from datetime import datetime


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
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for i, repo in enumerate(self.active_repos):
            description = repo.description or "No description available"
            alignment = "left" if i % 2 == 0 else "right"
            float_direction = "left" if i % 2 == 0 else "right"
            
            self.working_on_section += f"""<div align="{alignment}" style="width: 48%; float: {float_direction}; clear: both; margin-bottom: 20px; border: 1px solid #2f80ed; border-radius: 10px; padding: 16px; background-color: #0d1117;">
  <h3><a href="{repo.html_url}">{repo.name}</a></h3>
  <p>{description}</p>
</div>\n\n"""
        
        self.working_on_section += """<div style="clear: both;"></div>

<p align="right"><em>Last updated: """ + current_date + """</em></p>

"""

    def update_readme(self):
        content = self.readme
        working_on_section = self.working_on_section

        full_pattern = r'<div style="padding: 15px; margin-top: 20px; margin-bottom: 20px;">\s*\n*\s*## 🚀 Working on:[\s\S]*?<\/div>'
        
        replacement = '<div style="padding: 15px; margin-top: 20px; margin-bottom: 20px;">\n\n' + working_on_section + '</div>'
        
        if re.search(full_pattern, content):
            updated_content = re.sub(full_pattern, replacement, content)
        else:
            if "# " in content or "<h1" in content:
                if "<h1" in content:
                    pos = content.find("<h1")
                    pos = content.find("</h1>", pos) + 6
                else:
                    pos = content.find("# ")
                    pos = content.find("\n", pos) + 1
                
                updated_content = content[:pos] + "\n\n" + replacement + "\n\n" + content[pos:]
            else:
                updated_content = replacement + "\n\n" + content

        with open(self.readme_path, "w") as f:
            f.write(updated_content)