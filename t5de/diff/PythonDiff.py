import os
import shutil
import zipfile
import difflib

from uncompyle6 import decompile_file

from .Diff import Diff


class PythonDiff(Diff):
    def setup(self):
        self._process(self.previous, self.previous_cwd)
        self._process(self.current, self.current_cwd)

    def diff(self):
        print('DIFFING: IMVU {} and IMVU {}'.format(self.previous, self.current))
        print('\tDIFFING: IMVUCLIENT')

        previous = os.path.join(self.cwd, 'library-{}'.format(self.previous))
        current = os.path.join(self.cwd, 'library-{}'.format(self.current))

        for root, dirs, files in os.walk(previous):
            for f in files:
                if f.endswith('.pyc') or f.endswith('.pyo'):
                    continue

                previous_file = os.path.join(root, f)
                current_file = os.path.join(root.replace(self.previous, self.current), f)

                if not os.path.isfile(current_file):
                    print('\t\tREMOVED: {}'.format(f))
                    continue

                with open(previous_file, 'r') as previous_file:
                    with open(current_file, 'r') as current_file:
                        diff = difflib.unified_diff(
                            previous_file.readlines(), current_file.readlines(),
                            fromfile=previous_file.name, tofile=current_file.name
                        )

                        for line in diff:
                            print(line)

    def cleanup(self):
        shutil.rmtree('library-{}'.format(self.previous))
        shutil.rmtree('library-{}'.format(self.current))

    def _process(self, version, cwd):
        print('PROCESSING: {}'.format(version))
        print('\tEXTRACTING: LIBRARY.ZIP')

        if os.path.isdir('{}/library'.format(self.cwd)):
            shutil.rmtree('{}/library'.format(self.cwd))

        with zipfile.ZipFile('{}/library.zip'.format(cwd), 'r') as zip_file:
            zip_file.extractall('{}/library'.format(self.cwd))

        print('\tDECOMPILING: LIBRARY')
        self._decompile('imvu')
        self._decompile('main')

        print('\tMOVING: LIBRARY')
        if os.path.isdir('{}/library-{}'.format(self.cwd, version)):
            shutil.rmtree('{}/library-{}'.format(self.cwd, version))
        shutil.move('{}/library'.format(self.cwd), '{}/library-{}'.format(self.cwd, version))

    def _decompile(self, subdir):
        """
        :param str subdir:
        """
        print('\t\tDECOMPILING: {}'.format(subdir))
        for root, dirs, files in os.walk('{}/library/{}'.format(self.cwd, subdir)):
            for compiled in files:
                if compiled.endswith('.pyo'):
                    if os.path.isfile(os.path.join(root, os.path.splitext(compiled)[0] + '.py')):
                        continue
                    path = os.path.join(root, os.path.splitext(compiled)[0] + '.py')
                    with open(path, "w") as output:
                        try:
                            decompile_file(os.path.join(root, compiled), output, showasm=False)
                        except Exception as e:
                            continue
