import inspect
import os

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
        pass

    def cleanup(self):
        print('REMOVING: DEVICEFINGERPRINT.EXE')
        os.remove(os.path.join(self.cwd, 'IMVUClient', 'devicefingerprint.exe'))
