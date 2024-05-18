import os
import requests

from bs4 import BeautifulSoup

VERSION_PATH = '{}\\VERSION'.format(os.getcwd())
VERSION_URL = 'https://www.imvu.com/download.php'

if __name__ == '__main__':
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
    else:
        print('NO UPDATE AVAILABLE')
