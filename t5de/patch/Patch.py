from typing import List, NamedTuple
from .. import Context

Replacement = NamedTuple("Replacement", [('name', str), ('pattern', str), ('path', str)])


class Patch(object):
    """
    Base class for patches, a collection of replacements to apply to a file or files.
    """

    def __init__(self):
        self.replacements = []  # type: List[Replacement]

    def register(self, name, filename, pattern):
        """
        Register a replacement to apply to a file.
        :param str name:
        :param str filename:
        :param str pattern:
        :return:
        """
        self.replacements.append(Replacement(name, pattern, filename))

    def setup(self, context):
        """
        Called to set up the patch, this is called before the patch is applied.
        :param Context.Context context:
        :return:
        """
        pass

    def apply(self, context):
        """
        :param Context context:
        :return:
        """
        self.patch(context)

    def patch(self, context):
        """
        :param Context context:
        :return:
        """
        pass

    def cleanup(self, context):
        """
        :param Context context:
        :return:
        """
        pass
