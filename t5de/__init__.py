import os
import re
import shutil
import time

import autogui
import requests


class Patcher:
    BASE_URL = 'https://static-akm.imvu.com/imvufiles/installers/InstallIMVU_{}.exe'
    CLIENT_PATH = '{}/IMVUClient'.format(os.getenv('APPDATA'))

    def __init__(self, cwd, version):
        self.cwd = cwd
        self.version = version

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def download(self):
        print('DOWNLOADING: IMVU {}'.format(self.version))
        if os.path.isfile(os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version)):
            return

        r = requests.get(Patcher.BASE_URL.format(self.version))

        with open(os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version), 'wb') as f:
            f.write(r.content)

    def install(self):
        print('INSTALLING: IMVU {}'.format(self.version))
        autogui.open(os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version), setActive=False)
        autogui.setWindow('IMVU Setup')
        autogui.click('Install', 0, 4)
        print('SLEEPING: 15 SECONDS...')
        time.sleep(15)

        attempts = 0
        while attempts < 5:
            attempts += 1
            try:
                autogui.setWindow('IMVU Login')
                autogui.click('Close', 0, 4)
                break
            except Exception:
                if attempts > 5:
                    raise RuntimeError('Could not automate IMVU install! Failed to find Login window.')
                print('SLEEPING: 5 SECONDS...')
                time.sleep(5)

        print('INSTALLED: IMVU {}'.format(self.version))

    def copy(self):
        print('COPYING: {}'.format(Patcher.CLIENT_PATH))
        if not os.path.isdir(os.path.join(self.cwd, 'IMVUClient')):
            shutil.copytree(
                Patcher.CLIENT_PATH, os.path.join(self.cwd, 'IMVUClient'), ignore=shutil.ignore_patterns('*.lock')
            )

    def patch(self, patchers):
        for patcher in patchers:
            patcher.setup(self.cwd)

        for patcher in patchers:
            for p in patcher.patches():
                output = []

                print('PATCHING: {}'.format(p.file))

                with open(os.path.join(self.cwd, p.dir, p.file + p.ext)) as f:
                    source = f.readlines()

                    i = 0
                    while i < len(source):
                        line = source[i]
                        found = False
                        for name, pattern in p.patterns.iteritems():
                            if re.search(pattern, line):
                                print('PATCHED: {} in {}'.format(name, p.file))
                                found = True
                                i = p.apply(line, pattern=name, index=i, source=source, output=output)
                                break
                        i += 1
                        if not found:
                            output.append(line)

                with open(os.path.join(self.cwd, p.dir, p.file + p.ext), "w") as f:
                    f.writelines(output)

        for patcher in patchers:
            patcher.cleanup(self.cwd)

    def cleanup(self):
        executable = os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version)
        if os.path.isfile(executable):
            os.remove(executable)
        client_dir = os.path.join(self.cwd, 'IMVUClient')
        if os.path.isdir(client_dir):
            shutil.rmtree(client_dir)
