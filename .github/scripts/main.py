import os
from repo import Repository
from philosophy import Philosophy

oculted_repos_str = os.getenv("OCULTED_REPOS", "")
oculted_repos = [repo.strip() for repo in oculted_repos_str.split(",")] if oculted_repos_str else []

working_on_section = "## 🚀 Working on:\n\n"

repo = Repository(
    username=os.getenv("GITHUB_USERNAME"),
    token=os.getenv("GITHUB_TOKEN"),
    oculted_repos=oculted_repos,
    working_on_section=working_on_section
)

try:
    repo.prepare_readme()
    repo.populate_active_repos()
    repo.append_working_section()
    repo.update_readme()
    print("README.md updated successfully!")
except Exception as e:
    print(f"Error updating README: {e}")
    exit(1)

count = Philosophy.get_count()
quote = Philosophy.get_quote(count)

Philosophy.update_h1(quote)
