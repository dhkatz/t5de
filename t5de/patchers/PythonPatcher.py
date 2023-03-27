import inspect
import os
import shutil
import zipfile

from .Patcher import Patcher
from ..patches import python as python_patches


class PythonPatcher(Patcher):
    """
    Extracts the library.zip file from the IMVUClient directory,
    decompiles the python files, applies the patches, recompiles the python files, and then re-archives the library.zip
    """

    def __init__(self, cwd):
        super(PythonPatcher, self).__init__(
            cwd,
            [cls() for name, cls in inspect.getmembers(python_patches, inspect.isclass)]
        )

    def setup(self):
        print('EXTRACTING: LIBRARY.ZIP')

        if os.path.isdir('{}/library'.format(self.cwd)):
            shutil.rmtree('{}/library'.format(self.cwd))

        with zipfile.ZipFile('{}/IMVUClient/library.zip'.format(self.cwd), 'r') as zip_file:
            zip_file.extractall('{}/library'.format(self.cwd))

    def cleanup(self):
        print('ARCHIVING: LIBRARY.ZIP')

        lib_dir = os.path.join(self.cwd, 'library')

        with zipfile.ZipFile(os.path.join(self.cwd, 'library.zip'), 'w', compression=zipfile.ZIP_STORED) as zip_file:
            for root, dirs, files in os.walk(lib_dir):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    zip_file.write(filepath, os.path.relpath(filepath, lib_dir))

        print('ARCHIVED: LIBRARY.ZIP')

        print('REPLACING: LIBRARY.ZIP')

        os.remove(os.path.join(self.cwd, 'IMVUClient', 'library.zip'))
        shutil.move(os.path.join(self.cwd, 'library.zip'), os.path.join(self.cwd, 'IMVUClient'))
        shutil.rmtree(os.path.join(self.cwd, 'library'))
