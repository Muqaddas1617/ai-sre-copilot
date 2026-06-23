class MemoryAgent:
    name = "Memory Agent"

    def __init__(self, persisted_history=None):
        self.history = list(persisted_history or [])

    def add_entry(self, text: str):
        if not text or not isinstance(text, str):
            return None
        entry = text.strip().lower()
        if entry not in self.history:
            self.history.append(entry)
        return entry

    def lookup(self, keyword: str):
        if not keyword or not isinstance(keyword, str):
            return []
        keyword = keyword.lower()
        return [item for item in self.history if keyword in item]
