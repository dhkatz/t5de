import inspect
import os
import shutil

from .Patcher import Patcher
from ..patches import checksum as checksum_patches


class ChecksumPatcher(Patcher):
    def __init__(self, cwd):
        """
        :param str cwd:
        """
        super(ChecksumPatcher, self).__init__(
            cwd,
            [cls() for name, cls in inspect.getmembers(checksum_patches, inspect.isclass)]
        )

    def setup(self):
        print('COPYING: CHECKSUM.TXT')
        shutil.copy(os.path.join(self.cwd, 'IMVUClient', 'checksum.txt'), os.path.join(self.cwd, 'checksum.txt'))

    def cleanup(self):
        print('REPLACING: CHECKSUM.TXT')
        shutil.copy(os.path.join(self.cwd, 'checksum.txt'), os.path.join(self.cwd, 'IMVUClient', 'checksum.txt'))
        print('REMOVING: CHECKSUM.TXT')
        os.remove(os.path.join(self.cwd, 'checksum.txt'))

        print('REMOVING: DEVICEFINGERPRINT.EXE')
        os.remove(os.path.join(self.cwd, 'IMVUClient', 'devicefingerprint.exe'))
