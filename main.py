# coding=utf-8

import os
import shutil
import sys
import re
import zipfile
import requests
import autogui
import time

from uncompyle6 import decompile_file
from py_compile import compile

from patch import ClientAppPatch, AccountPatch, ProductLoaderPatch, WindowsPatch, SessionWindowPatch

PATH = os.path.dirname(sys.argv[0])
BASE_URL = 'https://static-akm.imvu.com/imvufiles/installers/InstallIMVU_{}.exe'
CLIENT_PATH = '{}/IMVUClient'.format(os.getenv('APPDATA'))
VERSION = '539.14'
PATCHES = [AccountPatch(), ClientAppPatch(), ProductLoaderPatch(), WindowsPatch(), SessionWindowPatch()]


def download():
    print('DOWNLOADING: IMVU {}'.format(VERSION))
    if os.path.isfile('{}/InstallIMVU_{}.exe'.format(PATH, VERSION)):
        return

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


def copy():
    print('COPYING: {}'.format(CLIENT_PATH))
    if not os.path.isdir(os.path.join(PATH, 'IMVUClient')):
        shutil.copytree(CLIENT_PATH, os.path.join(PATH, 'IMVUClient'))


def extract():
    print('EXTRACTING: LIBRARY.ZIP')
    with zipfile.ZipFile('{}/IMVUClient/library.zip'.format(PATH), 'r') as zip_file:
        zip_file.extractall('{}/library'.format(PATH))


def decompile():
    for p in PATCHES:
        print('DECOMPILING: {}'.format(p.file))
        with open("{}/library/{}.py".format(PATH, p.file), "w") as f:
            decompile_file("{}/library/{}.pyo".format(PATH, p.file), f)


def patch():
    for p in PATCHES:
        output = []

        print('PATCHING: {}'.format(p.file))

        with open("{}/library/{}.py".format(PATH, p.file)) as f:
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

        with open("{}/library/{}.py".format(PATH, p.file), "w") as f:
            f.writelines(output)


def recompile():
    for p in PATCHES:
        print('COMPILING: {}'.format(p.file))
        compile('{}/library/{}.py'.format(PATH, p.file), '{}/library/{}.pyo'.format(PATH, p.file), '-o', doraise=True)


def cleanup():
    for p in PATCHES:
        print('CLEANING: {}'.format(p.file))
        filepath = '{}/library/{}.py'.format(PATH, p.file)
        if os.path.isfile(filepath):
            os.remove(filepath)


def archive():
    print('ARCHIVING: LIBRARY.ZIP')

    lib_dir = os.path.join(PATH, 'library')

    with zipfile.ZipFile(os.path.join(PATH, 'library.zip'), 'w', compression=zipfile.ZIP_STORED) as zip_file:
        for root, dirs, files in os.walk(lib_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                zip_file.write(filepath, os.path.relpath(filepath, lib_dir))

    print('ARCHIVED: LIBRARY.ZIP')


def replace():
    print('REPLACING: LIBRARY.ZIP')

    os.remove(os.path.join(PATH, 'IMVUClient', 'library.zip'))
    shutil.move(os.path.join(PATH, 'library.zip'), os.path.join(PATH, 'IMVUClient'))


if __name__ == '__main__':
    download()
    install()
    copy()
    extract()
    decompile()
    patch()
    recompile()
    cleanup()
    archive()
    replace()
