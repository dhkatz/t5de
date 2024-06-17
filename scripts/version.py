import os
import sys
import argparse

import requests

from bs4 import BeautifulSoup

VERSION_PATH = '{}\\VERSION'.format(os.getcwd())
VERSION_URL = 'https://www.imvu.com/download.php'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check for updates')
    parser.add_argument('--latest', action='store_true', help='Print the latest version')
    parser.add_argument('--current', action='store_true', help='Print the current version')
    parser.add_argument('--update', action='store_true', help='Check for updates')

    args = parser.parse_args()

    if args.latest:
        response = requests.get(VERSION_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        h2 = soup.find('h2', text='IMVU Classic:')
        b = h2.find_next('b')
        latest_version = b.text.strip(':')
        print(latest_version)
        sys.exit(0)

    if args.current:
        with open(VERSION_PATH, 'r') as f:
            version = f.read().strip()
            print(version)
            sys.exit(0)

    cwd = os.getcwd()

    print('READING VERSION: {}'.format(VERSION_PATH))

    with open(VERSION_PATH, 'r') as f:
        version = f.read().strip()
        print('VERSION: {}'.format(version))

    response = requests.get(VERSION_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    h2 = soup.find('h2', text='IMVU Classic:')
    b = h2.find_next('b')
    latest_version = b.text.strip(':')

    print('LATEST VERSION: {}'.format(latest_version))

    if version != latest_version:
        print('UPDATE AVAILABLE')
        sys.exit(1)
    else:
        print('NO UPDATE AVAILABLE')
        sys.exit(0)
