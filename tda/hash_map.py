class HashMap:
    def __init__(self, size=100):
        self.table = [[] for _ in range(size)]
    def _hash(self, key):
        return hash(key) % len(self.table)
    def set(self, key, value):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        self.table[idx].append((key, value))
    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        raise KeyError(key)