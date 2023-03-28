import os
import shutil
import zipfile

from uncompyle6 import decompile_file

CLIENT_PATH = '{}/IMVUClient'.format(os.getenv('APPDATA'))

if __name__ == '__main__':
    cwd = os.getcwd()

    print('COPYING: {}'.format(CLIENT_PATH))

    if os.path.isdir(os.path.join(cwd, 'IMVUClient')):
        shutil.rmtree(os.path.join(cwd, 'IMVUClient'))

    shutil.copytree(
        CLIENT_PATH, os.path.join(cwd, 'IMVUClient'),
        ignore=shutil.ignore_patterns('*.lock')
    )

    print('EXTRACTING: LIBRARY.ZIP')

    if os.path.isdir('{}/library'.format(cwd)):
        shutil.rmtree('{}/library'.format(cwd))

    with zipfile.ZipFile('{}/IMVUClient/library.zip'.format(cwd), 'r') as zip_file:
        zip_file.extractall('{}/library'.format(cwd))

    print('DECOMPILING: LIBRARY')

    for root, dirs, files in os.walk('{}/library/imvu'.format(cwd)):
        for compiled in files:
            print('DECOMPILING: {}'.format(compiled))
            if compiled.endswith('.pyo'):
                path = os.path.join(root, os.path.splitext(compiled)[0] + '.py')
                with open(path, "w") as output:
                    try:
                        decompile_file(os.path.join(root, compiled), output, showasm=False)
                    except Exception as e:
                        print('SKIPPING: {} (error)'.format(compiled))
                        continue
