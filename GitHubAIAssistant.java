// GitHubAIAssistant.java
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;

public class GitHubAIAssistant {
    private Set<String> supportedLanguages;
    private List<Map<String, String>> issuesFound;
    
    public GitHubAIAssistant() {
        this.supportedLanguages = Set.of(
            "python", "java", "javascript", "typescript", "html",
            "css", "cpp", "c", "csharp", "go", "rust", "ruby"
        );
        this.issuesFound = new ArrayList<>();
    }
    
    public Map<String, Object> analyzeRepository(String repoPath) throws IOException {
        Map<String, Object> analysis = new HashMap<>();
        analysis.put("totalFiles", 0);
        analysis.put("complexityScore", 0);
        
        Map<String, Integer> byLanguage = new HashMap<>();
        analysis.put("byLanguage", byLanguage);
        
        Files.walk(Paths.get(repoPath))
            .filter(Files::isRegularFile)
            .forEach(filePath -> {
                String language = detectLanguage(filePath.toString());
                
                if (language != null && supportedLanguages.contains(language)) {
                    byLanguage.put(language, byLanguage.getOrDefault(language, 0) + 1);
                    analysis.put("totalFiles", (Integer)analysis.get("totalFiles") + 1);
                    
                    try {
                        int complexity = analyzeFileComplexity(filePath, language);
                        analysis.put("complexityScore", (Integer)analysis.get("complexityScore") + complexity);
                    } catch (IOException e) {
                        System.err.println("Ошибка анализа файла: " + filePath);
                    }
                }
            });
        
        analysis.put("issuesFound", new ArrayList<>(issuesFound));
        return analysis;
    }
    
    private String detectLanguage(String filePath) {
        Map<String, String> extensionMap = Map.ofEntries(
            Map.entry(".py", "python"),
            Map.entry(".java", "java"),
            Map.entry(".js", "javascript"),
            Map.entry(".ts", "typescript"),
            Map.entry(".html", "html"),
            Map.entry(".css", "css"),
            Map.entry(".cpp", "cpp"),
            Map.entry(".c", "c"),
            Map.entry(".cs", "csharp"),
            Map.entry(".go", "go"),
            Map.entry(".rs", "rust"),
            Map.entry(".rb", "ruby")
        );
        
        int dotIndex = filePath.lastIndexOf('.');
        if (dotIndex > 0) {
            String extension = filePath.substring(dotIndex);
            return extensionMap.get(extension);
        }
        return null;
    }
    
    private int analyzeFileComplexity(Path filePath, String language) throws IOException {
        List<String> lines = Files.readAllLines(filePath);
        int complexity = lines.size() / 10;
        
        // Проверка качества кода
        String content = String.join("\n", lines);
        if ("java".equals(language)) {
            if (content.contains("System.out.println") && content.contains("e.printStackTrace()")) {
                addIssue("Возможно избыточное логирование", "warning");
            }
        }
        
        return complexity;
    }
    
    private void addIssue(String message, String severity) {
        Map<String, String> issue = new HashMap<>();
        issue.put("message", message);
        issue.put("severity", severity);
        issuesFound.add(issue);
    }
    
    public static void main(String[] args) {
        GitHubAIAssistant assistant = new GitHubAIAssistant();
        try {
            Map<String, Object> analysis = assistant.analyzeRepository(".");
            System.out.println("Анализ завершен:");
            System.out.println("Всего файлов: " + analysis.get("totalFiles"));
            System.out.println("По языкам: " + analysis.get("byLanguage"));
            System.out.println("Сложность: " + analysis.get("complexityScore"));
        } catch (IOException e) {
            System.err.println("Ошибка анализа репозитория: " + e.getMessage());
        }
    }
}
