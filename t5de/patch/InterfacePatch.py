from . import Patch


class InterfacePatch(Patch):
    """
    Base class for interface patches.

    An interface patch is a patch that modifies the UI of the game. This may include HTML, CSS, or JS.
    """

    def register(self, name, filename, pattern):
        if filename.startswith("imvuContent/"):
            filename = filename[12:]

        super(InterfacePatch, self).register(name, "imvuContent/{}".format(filename), pattern)

    def setup(self, context):
        pass

    def cleanup(self, context):
        pass
