import os
import shutil
import time

import autogui
import requests
from bs4 import BeautifulSoup

from typing import List


# noinspection PyBroadException
class Client:
    """
    A class to manage the IMVU client

    Attributes:
        cwd (str): The current working directory
        version (str): The version of IMVU to manipulate
    """

    BASE_URL = 'https://static-akm.imvu.com/imvufiles/installers/InstallIMVU_{}.exe'
    VERSION_URL = 'https://www.imvu.com/download.php'
    CLIENT_PATH = '{}/IMVUClient'.format(os.getenv('APPDATA'))

    def __init__(self, version=None, cwd=None):
        """
        :param str|None version: The version of IMVU to manipulate, if None, the latest version is used
        :param str|None cwd: The current working directory
        """
        self.cwd = cwd or os.getcwd()
        self.version = version or self._latest_version()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def download(self):
        """
        Download the IMVU client executable if it does not exist

        :return: True if the executable was downloaded, False otherwise
        :rtype: bool
        """
        print('DOWNLOADING: IMVU {}'.format(self.version))
        if os.path.isfile(os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version)):
            return False

        r = requests.get(Client.BASE_URL.format(self.version))

        with open(os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version), 'wb') as f:
            f.write(r.content)

        return True

    def install(self, download=False):
        """
        Install the IMVU client using the downloaded executable
        :param bool download: Download the executable if it does not exist
        """
        if not os.path.isfile(os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version)):
            if download:
                self.download()
            else:
                raise IOError('Could not find InstallIMVU_{}.exe'.format(self.version))

        print('INSTALLING: IMVU {}'.format(self.version))
        autogui.open(os.path.join(self.cwd, 'InstallIMVU_%s.exe' % self.version), setActive=False)
        attempts = 0
        while attempts < 5:
            attempts += 1
            try:
                autogui.setWindow('IMVU Setup')
                autogui.click('Install', 0, 4)
                break
            except Exception:
                if attempts > 5:
                    raise RuntimeError('Could not automate IMVU install! Failed to find Setup window.')
                print('SLEEPING: 5 SECONDS...')
                time.sleep(5)
        print('SLEEPING: 15 SECONDS...')
        time.sleep(15)

        attempts = 0
        while attempts < 5:
            attempts += 1
            try:
                if autogui.exists('Update Available'):
                    print('SKIPPING: UPDATE AVAILABLE PROMPT')
                    autogui.setWindow('Update Available', timeout=4)
                    autogui.click('Close', timeout=4)
                    time.sleep(5)
                autogui.setWindow('IMVU Login')
                autogui.click('Close', timeout=4)
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
        
        print('COPYING: devicefingerprint.pyd')
        
        shutil.copy(
            os.path.join(self.cwd, 'scripts/devicefingerprint.pyd'), os.path.join(self.cwd, 'IMVUClient')
        )

    def patch(self, patchers, dry_run=False):
        """
        Patch the IMVU client
        :param List patchers: A list of patchers to run
        :param bool dry_run: Do not apply patches, only simulate
        """
        if not os.path.isdir(os.path.join(self.cwd, 'IMVUClient')):
            raise IOError('Could not find IMVUClient directory')

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

    def diff(self, generators, version=None):
        """
        :param List[constructor] generators: A list of diff generators
        :param str version: The version to diff against, if None, the latest version is used
        """
        if version is None:
            version = self._latest_version()

        if self.version == version:
            print('SKIPPED: IMVU {} and IMVU {} are the same'.format(self.version, version))
            return

        if os.path.isdir(os.path.join(self.cwd, 'IMVUClient-{}'.format(self.version))):
            shutil.rmtree(os.path.join(self.cwd, 'IMVUClient-{}'.format(self.version)))

        print('DIFFING: IMVU {} and IMVU {}'.format(self.version, version))

        # Download the previous version first
        self.download()
        self.install()
        self.copy()

        # Rename the previous version to IMVUClient-{version}
        if os.path.isdir(os.path.join(self.cwd, 'IMVUClient-{}'.format(self.version))):
            shutil.rmtree(os.path.join(self.cwd, 'IMVUClient-{}'.format(self.version)))

        shutil.move(os.path.join(self.cwd, 'IMVUClient'), os.path.join(self.cwd, 'IMVUClient-{}'.format(self.version)))

        # Download the current version
        current_version = self.version
        self.version = version

        self.download()
        self.install()
        self.copy()

        # Rename the current version to IMVUClient-{current}
        if os.path.isdir(os.path.join(self.cwd, 'IMVUClient-{}'.format(version))):
            shutil.rmtree(os.path.join(self.cwd, 'IMVUClient-{}'.format(version)))

        shutil.move(os.path.join(self.cwd, 'IMVUClient'), os.path.join(self.cwd, 'IMVUClient-{}'.format(version)))

        self.version = current_version

        previous_cwd = os.path.join(self.cwd, 'IMVUClient-{}'.format(self.version))
        current_cwd = os.path.join(self.cwd, 'IMVUClient-{}'.format(version))

        for Generator in generators:
            print('PROCESSING DIFF GENERATOR: {}'.format(Generator.__name__))
            with Generator(self.cwd, self.version, version, previous_cwd, current_cwd) as generator:
                generator.diff()

        executable = os.path.join(self.cwd, 'InstallIMVU_%s.exe' % version)
        if os.path.isfile(executable):
            try:
                os.remove(executable)
            except Exception as e:
                print('ERROR: {}'.format(e))
                pass

    def _latest_version(self):
        """
        Get the latest version of IMVU
        :return: The latest version of IMVU
        :rtype: str
        """
        response = requests.get(Client.VERSION_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        h2 = soup.find('h2', text='IMVU Classic:')
        b = h2.find_next('b')
        return b.text.strip(':')
