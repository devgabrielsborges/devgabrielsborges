import re
from github import Github
from datetime import datetime


class Repository:
    """Classe para gerenciar os repositórios no GitHub e atualizar o README."""
    
    def __init__(
        self, username: str,
        token: str,
        oculted_repos: list[str],
        working_on_section: str,
        readme_path="README.md"
    ):
        """Inicializa a classe Repository.
        
        Args:
            username: Nome de usuário do GitHub
            token: Token de acesso do GitHub
            oculted_repos: Lista de repositórios a serem ocultados
            working_on_section: Título da seção de trabalho
            readme_path: Caminho para o arquivo README
        """
        self.username = username
        self.oculted_repos = oculted_repos
        self.user = Github(token).get_user(username)
        self.repos = self.get_repos()
        self.active_repos = []
        self.readme_path = readme_path
        self.readme = self.get_readme(self.readme_path)
        self.working_on_section = working_on_section

    def get_repos(self) -> list:
        """Obtém a lista de repositórios do usuário.
        
        Returns:
            Lista de objetos de repositório
        
        Raises:
            Exception: Se houver um erro ao buscar os repositórios
        """
        try:
            return list(self.user.get_repos(sort="updated"))
        except Exception as e:
            raise Exception(f"Repo fetching exception: {e}")

    def populate_active_repos(self):
        """Preenche a lista de repositórios ativos com base nos critérios."""
        for repo in self.repos:
            if not repo.fork and repo.name not in self.oculted_repos:
                self.active_repos.append(repo)
            if len(self.active_repos) >= 3:
                break

    def get_readme(self, path):
        """Obtém o conteúdo do arquivo README.
        
        Args:
            path: Caminho para o arquivo README
            
        Returns:
            Conteúdo do arquivo README
        """
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"# Hello, I'm {self.username}\n\n"

    def generate_card(self, repo, index):
        """Gera o HTML para um card de repositório.
        
        Args:
            repo: Objeto repositório
            index: Índice do repositório para alternância de layout
            
        Returns:
            String HTML do card
        """
        description = repo.description or "My latest project"
        alignment = "left" if index % 2 == 0 else "right"
        float_direction = "left" if index % 2 == 0 else "right"
        
        return f"""<div class="card" align="{alignment}" style="width: 48%; float: {float_direction}; clear: both; margin-bottom: 20px; border: 1px solid #2f80ed; border-radius: 10px; padding: 16px; background-color: #0d1117;">
  <h3><a href="{repo.html_url}">{repo.name}</a></h3>
  <p>{description}</p>
</div>\n\n"""

    def update_readme(self):
        """Atualiza o README.md com os repositórios ativos."""
        content = self.readme
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        section_pattern = r'<div style="padding: 15px; margin-top: 20px; margin-bottom: 20px;">\s*\n*\s*## 🚀 Working on:'
        section_match = re.search(section_pattern, content)
        
        if section_match:
            section_start = section_match.start()
            section_end = content.find("</div>", section_start) + 6
            
            section = content[section_start:section_end]
            
            card_pattern = r'<div class="card"[^>]*>[\s\S]*?</div>\s*\n*'
            existing_cards = re.findall(card_pattern, section)
            
            existing_repo_names = []
            for card in existing_cards:
                repo_name_match = re.search(r'<h3><a href="[^"]*">([^<]+)</a></h3>', card)
                if repo_name_match:
                    existing_repo_names.append(repo_name_match.group(1))
            
            active_repo_names = [repo.name for repo in self.active_repos]
            
            if set(existing_repo_names) == set(active_repo_names) and len(existing_repo_names) == len(active_repo_names):
                print("Repository list unchanged, only updating date")
                updated_content = re.sub(
                    r'<p align="right"><em>Last updated: .*?</em></p>',
                    f'<p align="right"><em>Last updated: {current_date}</em></p>',
                    content
                )
            else:
                new_cards = ""
                for i, repo in enumerate(self.active_repos):
                    new_cards += self.generate_card(repo, i)
                
                new_section = f'''<div style="padding: 15px; margin-top: 20px; margin-bottom: 20px;">

## 🚀 Working on:

{new_cards}<div style="clear: both;"></div>

<p align="right"><em>Last updated: {current_date}</em></p>

</div>'''
                
                updated_content = content[:section_start] + new_section + content[section_end:]
                print(f"Replaced {len(existing_cards)} cards with {len(self.active_repos)} new cards")
        else:
            head_pattern = r'^[\s\S]*?</h1>\s*\n*'
            head_match = re.search(head_pattern, content)
            
            if head_match:
                head_end = head_match.end()
                
                new_cards = ""
                for i, repo in enumerate(self.active_repos):
                    new_cards += self.generate_card(repo, i)
                
                new_section = f'''

<div style="padding: 15px; margin-top: 20px; margin-bottom: 20px;">

## 🚀 Working on:

{new_cards}<div style="clear: both;"></div>

<p align="right"><em>Last updated: {current_date}</em></p>

</div>

'''
                updated_content = content[:head_end] + new_section + content[head_end:]
                print(f"Added new 'Working on' section with {len(self.active_repos)} cards")
            else:
                updated_content = content
                print("Warning: Could not find header section.")
        
        with open(self.readme_path, "w") as f:
            f.write(updated_content)
        print(f"README updated successfully: {self.readme_path}")

    def append_working_section(self):
    """
    Gera a seção "Working on" do README.
    Este método é mantido para compatibilidade com scripts existentes.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    new_cards = ""
    for i, repo in enumerate(self.active_repos):
        new_cards += self.generate_card(repo, i)
    
    self.working_on_section = f"""## 🚀 Working on:

{new_cards}<div style="clear: both;"></div>

<p align="right"><em>Last updated: {current_date}</em></p>
"""
    print(f"Generated content for {len(self.active_repos)} repositories")
