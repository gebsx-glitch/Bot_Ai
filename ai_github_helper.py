# ai_github_helper.py
import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional
import requests

class GitHubAIAssistant:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.supported_languages = {
            'python', 'java', 'javascript', 'typescript', 'html', 
            'css', 'cpp', 'c', 'csharp', 'go', 'rust', 'ruby',
            'php', 'swift', 'kotlin', 'scala', 'r', 'matlab'
        }
    
    def analyze_repository(self, repo_path: str) -> Dict:
        """Анализирует репозиторий и возвращает статистику"""
        analysis = {
            'total_files': 0,
            'by_language': {},
            'complexity_score': 0,
            'issues_found': []
        }
        
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = Path(root) / file
                language = self.detect_language(file_path)
                
                if language:
                    analysis['total_files'] += 1
                    analysis['by_language'][language] = analysis['by_language'].get(language, 0) + 1
                    
                    # Анализ сложности файла
                    complexity = self.analyze_file_complexity(file_path, language)
                    analysis['complexity_score'] += complexity
        
        return analysis
    
    def detect_language(self, file_path: Path) -> Optional[str]:
        """Определяет язык программирования по расширению файла"""
        extensions = {
            '.py': 'python',
            '.java': 'java',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'matlab'
        }
        return extensions.get(file_path.suffix.lower())
    
    def analyze_file_complexity(self, file_path: Path, language: str) -> int:
        """Анализирует сложность файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Простая метрика сложности
                complexity = len(lines) // 10  # Упрощенная метрика
                
                # Поиск потенциальных проблем
                if language == 'python':
                    if 'eval(' in content and 'input(' in content:
                        self.add_issue('Возможная уязвимость безопасности: eval с input')
                
                return complexity
                
        except Exception as e:
            print(f"Ошибка анализа файла {file_path}: {e}")
            return 0
    
    def add_issue(self, message: str):
        """Добавляет найденную проблему"""
        self.issues_found.append({
            'message': message,
            'severity': 'warning'
        })
    
    def generate_documentation(self, file_path: str) -> str:
        """Генерирует документацию для файла"""
        language = self.detect_language(Path(file_path))
        if language == 'python':
            return self.generate_python_doc(file_path)
        elif language == 'java':
            return self.generate_java_doc(file_path)
        # Добавьте обработку других языков...
        
        return "Документация не сгенерирована для данного типа файла"
    
    def generate_python_doc(self, file_path: str) -> str:
        """Генерирует документацию для Python файла"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Простой генератор документации
            doc = f"# Документация для {file_path}\n\n"
            doc += "## Функции и классы:\n\n"
            
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') or line.strip().startswith('class '):
                    doc += f"- {line.strip()}\n"
            
            return doc
        except Exception as e:
            return f"Ошибка генерации документации: {e}"

# Пример использования
if __name__ == "__main__":
    assistant = GitHubAIAssistant()
    analysis = assistant.analyze_repository('.')
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
