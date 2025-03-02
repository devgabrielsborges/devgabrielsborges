#!/usr/bin/env python3
import os
import re
from datetime import datetime
from github import Github

g = Github(os.getenv('GITHUB_TOKEN'))

username = "devgabrielsborges"
user = g.get_user(username)

# Get repositories sorted by last updated
try:
    repos = list(user.get_repos(sort="updated"))
except Exception as e:
    print(f"Error fetching repositories: {e}")
    exit(1)

# Select top 3 most recently updated non-fork repositories
active_repos = []
for repo in repos:
    if not repo.fork:
        active_repos.append({
            'name': repo.name,
            'url': repo.html_url,
            'description': repo.description or "No description available",
            'updated_at': repo.updated_at,
        })
    if len(active_repos) >= 3:
        break

# Prepare the "Working on" section content with the new title
current_date = datetime.now().strftime("%Y-%m-%d")
working_on_section = f"## Working on: 🚀\n\n*Last updated: {current_date}*\n\n"

for repo in active_repos:
    working_on_section += f"- [{repo['name']}]({repo['url']}) - {repo['description']}\n"

working_on_section += "\n"

# Read the current README.md
try:
    with open("README.md", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = "# Hello, I'm " + username + "\n\n"

pattern = r"## Working on: 🚀\n\n[\s\S]*?(?=##|$)"

if re.search(pattern, content):
    updated_content = re.sub(pattern, working_on_section, content)
else:
    # If no "Working on" section exists, add it after the introduction
    if "##" in content:
        # Insert before the first ## heading
        position = content.find("##")
        updated_content = content[:position] + working_on_section + content[position:]
    else:
        # Append to the end if there are no ## headings
        updated_content = content + "\n" + working_on_section

with open("README.md", "w") as f:
    f.write(updated_content)
