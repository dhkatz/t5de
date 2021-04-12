class Patch:
    def __init__(self):
        self.file = ""
        self.dir = ""
        self.ext = ""
        self.patterns = {}

    def apply(self, line, pattern, index, source, output):
        return index
