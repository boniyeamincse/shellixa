class HeliumSuggestionEngine:
    def __init__(self):
        self.command_map = {
            "": ["ls -la", "pwd", "whoami", "df -h", "systemctl status"],
            "git": ["git status", "git pull", "git checkout -b feature/", "git log --oneline --graph"],
            "docker": ["docker ps", "docker logs -f ", "docker exec -it  /bin/bash", "docker compose up -d"],
            "kubectl": ["kubectl get pods", "kubectl describe pod ", "kubectl logs -f ", "kubectl config current-context"],
            "systemctl": ["systemctl status ", "systemctl restart ", "systemctl enable ", "systemctl daemon-reload"],
            "journalctl": ["journalctl -u  -f", "journalctl -xe", "journalctl --since today"],
            "find": ["find . -maxdepth 2 -type f", "find /var/log -name '*.log'", "find . -type d | sort"],
            "grep": ["grep -Rin '' .", "grep -Rin 'error' /var/log", "grep -E 'WARN|ERROR' app.log"],
        }

    def suggest(self, text, history=None, snippets=None, limit=6):
        history = history or []
        snippets = snippets or []
        query = (text or "").strip()
        suggestions = []

        if not query:
            suggestions.extend(self.command_map[""])
        else:
            first_token = query.split()[0]
            for key, commands in self.command_map.items():
                if key and (first_token.startswith(key) or key.startswith(first_token)):
                    suggestions.extend(commands)
            suggestions.extend([item for item in history if item.startswith(query)])
            for snippet in snippets:
                if query.lower() in snippet["title"].lower() or query.lower() in snippet["tags"].lower():
                    suggestions.append(snippet["command"])

        unique = []
        seen = set()
        for item in suggestions:
            candidate = item.strip()
            if not candidate or candidate in seen:
                continue
            seen.add(candidate)
            unique.append(candidate)
            if len(unique) >= limit:
                break
        return unique
