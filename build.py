import os
import sys
import zipfile

PATH = os.path.dirname(sys.argv[0])


def archive():
    print('ARCHIVING: LIBRARY.ZIP')

    with zipfile.ZipFile('{}/library.zip', 'w', compression=zipfile.ZIP_STORED) as zip_file:
        zip_file.close()