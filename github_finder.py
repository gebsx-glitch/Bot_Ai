import requests
import json
from datetime import datetime

class GitHubFinder:
    def __init__(self):
        self.base_url = "https://api.github.com"
    
    def search_users(self, username, language=None, location=None):
        """Поиск пользователей по имени, языку и локации"""
        query = f"{username}"
        if language:
            query += f" language:{language}"
        if location:
            query += f" location:{location}"
        
        url = f"{self.base_url}/search/users"
        params = {
            'q': query,
            'per_page': 10
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()['items']
        except Exception as e:
            print(f"Ошибка: {e}")
            return []

    def get_user_details(self, username):
        """Получение детальной информации о пользователе"""
        url = f"{self.base_url}/users/{username}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except:
            return None

# Использование
if __name__ == "__main__":
    finder = GitHubFinder()
    
    # Поиск пользователей
    users = finder.search_users(
        username="Christian", 
        language="Python",
        location="Berlin"
    )
    
    print("Найденные пользователи:")
    for user in users:
        details = finder.get_user_details(user['login'])
        if details:
            print(f"👤 {user['login']}")
            print(f"   📝 Имя: {details.get('name', 'Не указано')}")
            print(f"   📍 Локация: {details.get('location', 'Не указана')}")
            print(f"   🔗 Профиль: {user['html_url']}")
            print("---")
