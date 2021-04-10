import os
import sys
import time
import zipfile

import requests
import autogui

PATH = os.path.dirname(sys.argv[0])
BASE_URL = 'https://static-akm.imvu.com/imvufiles/installers/InstallIMVU_{}.exe'
CLIENT_PATH = '{}/IMVUClient'.format(os.getenv('APPDATA'))
VERSION = '539.14'


def download():
    print('DOWNLOADING: IMVU {}'.format(VERSION))
    r = requests.get(BASE_URL.format(VERSION))

    with open('{}/{}'.format(PATH, 'InstallIMVU_{}.exe'.format(VERSION)), 'wb') as f:
        f.write(r.content)


def install():
    print('INSTALLING: IMVU {}'.format(VERSION))
    autogui.open('InstallIMVU_539.14.exe', setActive=False)
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

    print('INSTALLED: IMVU {}'.format(VERSION))


def extract():
    print('EXTRACTING: LIBRARY.ZIP')
    with zipfile.ZipFile('{}/library.zip'.format(CLIENT_PATH), 'r') as zip_file:
        zip_file.extractall('{}/library'.format(PATH))
