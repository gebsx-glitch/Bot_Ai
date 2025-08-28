from github_finder import GitHubFinder
import json

def main():
    finder = GitHubFinder()
    
    # Чтение конфига
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Поиск по разным языкам
    languages = config['search_options']['languages']
    
    for lang in languages:
        print(f"\n🔍 Поиск пользователей с языком {lang.upper()}:")
        users = finder.search_users("", language=lang)
        
        for user in users[:5]:  # Первые 5 результатов
            details = finder.get_user_details(user['login'])
            if details:
                print(f"   {user['login']} - {details.get('name', '')}")

if __name__ == "__main__":
    main()
