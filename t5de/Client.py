import os
import shutil
import time

import autogui
import requests

from typing import List


class Client:
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

        r = requests.get(Client.BASE_URL.format(self.version))

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
        print('COPYING: {}'.format(Client.CLIENT_PATH))

        if os.path.isdir(os.path.join(self.cwd, 'IMVUClient')):
            shutil.rmtree(os.path.join(self.cwd, 'IMVUClient'))

        shutil.copytree(
            Client.CLIENT_PATH, os.path.join(self.cwd, 'IMVUClient'),
            ignore=shutil.ignore_patterns('*.lock')
        )

    def patch(self, patchers, dry_run=False):
        """
        :param List patchers:
        :param dry_run:
        :return:
        """
        for Patcher in patchers:
            patcher = Patcher(self.cwd)
            patcher.setup()
            print('PROCESSING PATCHER: {}'.format(Patcher.__name__))
            patcher.patch(dry_run)
            patcher.cleanup()

    def cleanup(self):
        executable = os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version)
        if os.path.isfile(executable):
            os.remove(executable)
