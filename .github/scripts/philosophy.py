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
    def get_quote(count: int) -> str:
        body = ""
        try:
            while body == "" or len(body) > 60:
                response = requests.get(f"https://philosophyapi.pythonanywhere.com/api/ideas/{randint(1, count or 10)}/").json()
                body = f"{response['quote']}\n{response['author']}"
        except Exception:
            body = "Attention is all you need"
        finally:
            return body

    @staticmethod
    def update_h1(quote: str, readme_path="README.md"):
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
