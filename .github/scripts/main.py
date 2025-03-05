from repo import Repository
from philosophy import Philosophy
import os

philosophy = Philosophy()
count = philosophy.get_count()
quote, author = philosophy.get_quote(count)

philosophy.update_h1(quote)
philosophy.create_author_h3(author)

oculted_repos_str = os.getenv("OCULTED_REPOS", "")
oculted_repos = [repo.strip() for repo in oculted_repos_str.split(",")] if oculted_repos_str else []

working_on_section = "## 🚀 Working on:\n\n"

repo = Repository(
    username=os.getenv("GITHUB_USERNAME"),
    token=os.getenv("GITHUB_TOKEN"),
    oculted_repos=oculted_repos,
    working_on_section=working_on_section
)

repo.populate_active_repos()
repo.append_working_section()
repo.update_readme()
