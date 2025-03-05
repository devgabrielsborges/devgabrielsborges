import os
from datetime import datetime
from repo import Repository

oculted_repos_str = os.getenv("OCULTED_REPOS", "")
oculted_repos = [repo.strip() for repo in oculted_repos_str.split(",")] if oculted_repos_str else []

current_date = datetime.now().strftime("%Y-%m-%d")
working_on_section = f"## Working on: 🚀\n\n*Last updated: {current_date}*\n\n"

repo = Repository(
    username=os.getenv("GITHUB_USERNAME"),
    token=os.getenv("GITHUB_TOKEN"),
    oculted_repos=oculted_repos,
    working_on_section=working_on_section
)

try:
    repo.populate_active_repos()
    repo.append_working_section()
    
    pattern = r"## Working on: 🚀\n\n[\s\S]*?(?=##|$)"
    
    repo.update_readme(pattern)
    
    print(f"README.md updated successfully with {len(repo.active_repos)} active repositories!")
except Exception as e:
    print(f"Error updating README: {e}")
    exit(1)
