import os.path
from typing import List


class Context:
    """
    The context stores the current state of the patching process
    """

    def __init__(self, cwd, replacement=None):
        """
        Initialize the context
        :param str cwd:
        :param Replacement replacement:
        """
        self.cwd = cwd
        self.replacement = replacement

        self.path = ""  # type: str
        self.source = []  # type: List[str]
        self.line = ""  # type: str
        self.index = 0  # type: int
        self.pattern = ""  # type: str

        self.output = []

        if self.replacement:
            self.open(self.replacement)

    def open(self, replacement):
        """
        :param Replacement replacement:
        :return:
        """
        path = os.path.join(self.cwd, replacement.path)
        if os.path.isfile(path):
            with open(path) as f:
                self.replacement = replacement
                self.path = path
                self.source = f.readlines()
                self.index = 0
                self.line = self.source[0]
                self.pattern = None
                self.output = []
        else:
            raise IOError("File not found: {}".format(path))

        return self

    def close(self):
        if self.path is None:
            raise AttributeError("No path specified")

        with open(self.path, "w") as f:
            f.writelines(self.output)

    def write(self, text, indent=0):
        """
        Write a line to the output
        :param str text:
        :param int indent:
        :return:
        """
        self.output.append("{}{}".format("\t" * indent, text))

    def seek(self, index, absolute=False):
        """
        Seek to a line in the source
        :param int index:
        :param bool absolute:
        :return:
        """
        if absolute:
            self.index = index
        else:
            self.index += index

        if self.index >= len(self.source):
            self.index = len(self.source)
            self.line = None
        else:
            self.line = self.source[self.index]

    def skip(self, count):
        """
        Skip a number of lines
        :param int count:
        :return:
        """
        self.seek(count, False)

    def flush(self):
        for line in self.lines():
            self.write(line)
            self.seek(1)

    def lines(self):
        return self

    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.source):
            raise StopIteration
        return self.line

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
