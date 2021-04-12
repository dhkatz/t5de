import os

from patch import Patch


class ChecksumPatch(Patch):
    def __init__(self):
        Patch.__init__(self)
        self.dir = 'IMVUClient'
        self.file = 'checksum'
        self.ext = '.txt'
        self.patterns = {
            'DISABLE_LIBRARY': 'library',
            'DISABLE_IMVUCONTENT': 'imvuContent',
            'DISABLE_FINGERPRINT': 'devicefingerprint'
        }

    def apply(self, line, pattern, index, source, output):
        return index


def setup(_):
    pass


def patches():
    return [ChecksumPatch()]


def cleanup(cwd):
    print('REMOVING: DEVICEFINGERPRINT.EXE')
    os.remove(os.path.join(cwd, 'IMVUClient', 'devicefingerprint.exe'))
