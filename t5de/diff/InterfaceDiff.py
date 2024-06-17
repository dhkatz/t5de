import os
import shutil
import zipfile
import difflib

from .Diff import Diff


class InterfaceDiff(Diff):
    def setup(self):
        print('EXTRACTING: IMVUCONTENT.jar')
        self._process(self.previous, self.previous_cwd)
        self._process(self.current, self.current_cwd)

    def diff(self):
        print('DIFFING: IMVU {} and IMVU {}'.format(self.previous, self.current))
        print('\tDIFFING: IMVUCONTENT')

        previous = os.path.join(self.cwd, 'imvuContent-{}'.format(self.previous))
        current = os.path.join(self.cwd, 'imvuContent-{}'.format(self.current))

        for root, dirs, files in os.walk(previous):
            for f in files:
                # Skip if extension is not css, js, or html
                if not f.endswith('.css') and not f.endswith('.js') and not f.endswith('.html'):
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
        shutil.rmtree('imvuContent-{}'.format(self.previous))
        shutil.rmtree('imvuContent-{}'.format(self.current))

    def _process(self, version, cwd):
        print('PROCESSING: {}'.format(version))
        print('\tEXTRACTING: IMVUCONTENT.jar')

        if os.path.isdir('{}/imvuContent'.format(self.cwd)):
            shutil.rmtree('{}/imvuContent'.format(self.cwd))

        with zipfile.ZipFile('{}/ui/chrome/imvuContent.jar'.format(cwd), 'r') as zip_file:
            zip_file.extractall('{}/imvuContent'.format(self.cwd))

        print('\tMOVING: IMVUCONTENT')
        if os.path.isdir('{}/imvuContent-{}'.format(self.cwd, version)):
            shutil.rmtree('{}/imvuContent-{}'.format(self.cwd, version))

        shutil.move('{}/imvuContent'.format(self.cwd), '{}/imvuContent-{}'.format(self.cwd, version))
