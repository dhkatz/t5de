import re

from .. import Context
from ..patch import Patch


class Patcher(object):
    """
    Base class for patchers

    Attributes:
        cwd (str): The current working directory
        patches (list[Patch]): A list of patches to apply
    """

    def __init__(self, cwd, patches=None):
        """
        :param str cwd:
        :param list[Patch] patches:
        """
        if patches is None:
            patches = []
        self.cwd = cwd
        self.patches = patches

    def setup(self):
        raise NotImplementedError

    def patch(self, dry_run=False):
        for patch in self.patches:
            self._patch(patch, dry_run)

    def cleanup(self):
        raise NotImplementedError

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def _patch(self, patch, dry_run=False):
        """
        :param Patch patch:
        :param bool dry_run:
        :return:
        """
        context = Context(self.cwd, dry_run=dry_run)
        patch.setup(context)
        for replacement in patch.replacements:
            with context.open(replacement):
                Patcher._patch_replacement(patch, context)
        patch.cleanup(context)

    @staticmethod
    def _patch_replacement(patch, context):
        """
        Apply a patch to a file
        :param Patch patch:
        :param Context context:
        :return:
        """
        replacement = context.replacement
        for line in context.lines():
            if re.search(replacement.pattern, line):
                print('PATCHING: {} ({})'.format(replacement.path, replacement.name))

                if not context.dry_run:
                    context.pattern = replacement.name
                    patch.apply(context)
                    context.pattern = None
                else:
                    context.write(context.line)

                context.skip(1)

                print('PATCHED: {} ({})'.format(replacement.path, replacement.name))

                break
            else:
                context.write(context.line)
                context.skip(1)
        else:
            print('NOT PATCHED: {} ({})'.format(replacement.path, replacement.name))
        context.flush()
