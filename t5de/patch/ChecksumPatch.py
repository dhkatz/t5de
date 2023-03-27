from . import Patch


class ChecksumPatch(Patch):
    """
    This patch is used to disable the checksum verification for the library, imvuContent, and devicefingerprint files.
    """

    def patch(self, context):
        pass
