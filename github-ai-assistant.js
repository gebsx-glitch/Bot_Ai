// github-ai-assistant.js
const fs = require('fs');
const path = require('path');

class GitHubAIAssistant {
    constructor() {
        this.supportedLanguages = new Set([
            'python', 'java', 'javascript', 'typescript', 'html',
            'css', 'cpp', 'c', 'csharp', 'go', 'rust', 'ruby'
        ]);
    }

    async analyzeRepository(repoPath) {
        const analysis = {
            totalFiles: 0,
            byLanguage: {},
            complexityScore: 0,
            issuesFound: []
        };

        try {
            const files = await this.walkDirectory(repoPath);
            
            for (const file of files) {
                const language = this.detectLanguage(file);
                
                if (language && this.supportedLanguages.has(language)) {
                    analysis.totalFiles++;
                    analysis.byLanguage[language] = (analysis.byLanguage[language] || 0) + 1;
                    
                    const complexity = await this.analyzeFileComplexity(file, language);
                    analysis.complexityScore += complexity;
                }
            }

            return analysis;
        } catch (error) {
            console.error('Ошибка анализа:', error);
            return analysis;
        }
    }

    detectLanguage(filePath) {
        const ext = path.extname(filePath).toLowerCase();
        const extensionMap = {
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
            '.rb': 'ruby'
        };
        return extensionMap[ext];
    }

    async analyzeFileComplexity(filePath, language) {
        try {
            const content = await fs.promises.readFile(filePath, 'utf8');
            const lines = content.split('\n');
            
            // Простая метрика сложности
            let complexity = Math.floor(lines.length / 10);
            
            // Проверка качества кода
            if (language === 'javascript') {
                if (content.includes('eval(') && content.includes('innerHTML')) {
                    this.addIssue('Возможная XSS уязвимость');
                }
            }
            
            return complexity;
        } catch (error) {
            console.error(`Ошибка анализа файла ${filePath}:`, error);
            return 0;
        }
    }

    addIssue(message) {
        this.issuesFound.push({
            message,
            severity: 'warning'
        });
    }

    walkDirectory(dir) {
        return new Promise((resolve, reject) => {
            const files = [];
            
            function walk(currentPath) {
                const items = fs.readdirSync(currentPath);
                
                for (const item of items) {
                    const fullPath = path.join(currentPath, item);
                    const stat = fs.statSync(fullPath);
                    
                    if (stat.isDirectory()) {
                        walk(fullPath);
                    } else {
                        files.push(fullPath);
                    }
                }
            }
            
            try {
                walk(dir);
                resolve(files);
            } catch (error) {
                reject(error);
            }
        });
    }
}

module.exports = GitHubAIAssistant;
