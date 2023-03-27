import inspect
import os
import shutil
import zipfile

from ..patches import interface
from .Patcher import Patcher


class InterfacePatcher(Patcher):
    """
    Extracts the imvuContent.jar file from the IMVUClient directory and replaces it with the imvuContent.jar file from
    the patches before then re-archiving the imvuContent.jar file and replacing the original imvuContent.jar file.
    """
    def __init__(self, cwd):
        """
        :param str cwd:
        """
        super(InterfacePatcher, self).__init__(
            cwd,
            [cls() for name, cls in inspect.getmembers(interface, inspect.isclass)]
        )

    def setup(self):
        print ('EXTRACTING: IMVUCONTENT.jar')
        with zipfile.ZipFile('{}/IMVUClient/ui/chrome/imvuContent.jar'.format(self.cwd), 'r') as zip_file:
            zip_file.extractall(os.path.join(self.cwd, 'imvuContent'))

    def cleanup(self):
        print('ARCHIVING: IMVUCONTENT.JAR')

        content_dir = os.path.join(self.cwd, 'imvuContent')

        with zipfile.ZipFile(os.path.join(self.cwd, 'imvuContent.jar'), 'w', compression=zipfile.ZIP_STORED) as z:
            for root, dirs, files in os.walk(content_dir):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    z.write(filepath, os.path.relpath(filepath, content_dir))

        print('ARCHIVED: IMVUCONTENT.JAR')

        print('REPLACING: IMVUCONTENT.jar')

        os.remove(os.path.join(self.cwd, 'IMVUClient/ui/chrome', 'imvuContent.jar'))
        shutil.move(os.path.join(self.cwd, 'imvuContent.jar'), os.path.join(self.cwd, 'IMVUClient/ui/chrome'))

        # shutil.rmtree(os.path.join(self.cwd, 'imvuContent'))
