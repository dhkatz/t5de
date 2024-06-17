from abc import ABCMeta, abstractmethod


class Diff(object):
    __metaclass__ = ABCMeta
    """
    Base class for diff generators

    Attributes:
        cwd (str): The current working directory
        previous (str): The previous version
        current (str): The current version
        previous_cwd (str): The previous version's working directory
        current_cwd (str): The current version's working directory
    """

    def __init__(self, cwd, previous, current, previous_cwd, current_cwd):
        """
        :param str cwd:
        :param str previous:
        :param str current:
        :param str previous_cwd:
        :param str current_cwd:
        """
        self.cwd = cwd
        self.previous = previous
        self.current = current
        self.previous_cwd = previous_cwd
        self.current_cwd = current_cwd

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def diff(self):
        """
        Generate a diff between the previous and current versions
        """
        raise NotImplementedError

    @abstractmethod
    def cleanup(self):
        raise NotImplementedError

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def _diff(self):
        self.diff()
