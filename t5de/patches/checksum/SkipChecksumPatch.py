from ...patch import ChecksumPatch


class SkipChecksumPatch(ChecksumPatch):
    def __init__(self):
        super(SkipChecksumPatch, self).__init__()
        self.register('SKIP_LIBRARY', 'checksum.txt', 'library')
        self.register('SKIP_IMVUCONTENT', 'checksum.txt', 'imvuContent')
        self.register('SKIP_FINGERPRINT', 'checksum.txt', 'devicefingerprint')
