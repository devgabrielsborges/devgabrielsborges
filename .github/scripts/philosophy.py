import requests
from random import randint
import re


class Philosophy:
    @staticmethod
    def get_count() -> int:
        try:
            count = requests.get("https://philosophyapi.pythonanywhere.com/api/ideas/").json()['count']
        except Exception:
            count = 0
        finally:
            return count

    @staticmethod
    def get_quote(count: int) -> tuple:
        body = ""
        author = "Unknown"
        try:
            while body == "" or len(body) > 60:
                response = requests.get(f"https://philosophyapi.pythonanywhere.com/api/ideas/{randint(1, count or 10)}/").json()
                body = response['quote']
                if 'author' in response:
                    author = response['author']
                elif 'philosopher' in response:
                    author = response['philosopher']
        except Exception:
            body = "Attention is all you need"
            author = "Vaswani et al."
        finally:
            return body, author

    @staticmethod
    def update_h1(quote: str, readme_path="README.md"):
        """Atualiza apenas o título h1 com a citação."""
        try:
            with open(readme_path, "r") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: README file not found at {readme_path}")
            return False

        md_pattern = r'# <img[^>]*> .*'
        html_pattern = r'<h1[^>]*><img[^>]*> .*?<\/h1>'

        if re.search(md_pattern, content):
            updated_content = re.sub(
                r'# (<img[^>]*>) .*',
                r'# \1 ' + quote,
                content
            )
        elif re.search(html_pattern, content):
            updated_content = re.sub(
                r'<h1([^>]*)>(<img[^>]*>) .*?<\/h1>',
                r'<h1\1>\2 ' + quote + r'</h1>',
                content
            )
        else:
            print("Error: Could not find H1 section in README")
            return False

        try:
            with open(readme_path, "w") as f:
                f.write(updated_content)
            return True
        except Exception as e:
            print(f"Error writing to README: {e}")
            return False

    @staticmethod
    def delete_author_h3(readme_path="README.md"):
        """Remove o h3 do autor, se existir."""
        try:
            with open(readme_path, "r") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: README file not found at {readme_path}")
            return False, None

        # Padrão para encontrar o h3 do autor
        author_pattern = r'<h3 align="center"><em>— .*?</em></h3>\s*\n*'

        if re.search(author_pattern, content):
            # Remove o h3 do autor
            updated_content = re.sub(author_pattern, '', content)

            try:
                with open(readme_path, "w") as f:
                    f.write(updated_content)
                print("Removed existing author h3")
                return True, updated_content
            except Exception as e:
                print(f"Error writing to README: {e}")
                return False, None
        else:
            # Não há h3 para remover
            return True, content

    @staticmethod
    def create_author_h3(author: str, readme_path="README.md"):
        success, content = Philosophy.delete_author_h3(readme_path)
        if not success:
            return False

        # Padrão para encontrar o final do h1
        html_pattern = r'<h1[^>]*>.*?<\/h1>'

        h1_match = re.search(html_pattern, content)
        if h1_match:
            h1_end_pos = h1_match.end()
            author_html = f'\n<h3 align="center"><em>— {author}</em></h3>\n'

            updated_content = content[:h1_end_pos] + author_html + content[h1_end_pos:]

            try:
                with open(readme_path, "w") as f:
                    f.write(updated_content)
                print(f"Added author h3: {author}")
                return True
            except Exception as e:
                print(f"Error writing to README: {e}")
                return False
        else:
            print("Error: Could not find H1 section in README")
            return False
