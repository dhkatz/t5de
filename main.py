# coding=utf-8

import os
import sys
import re

from uncompyle6 import decompile_file
from py_compile import compile

from patch import ClientAppPatch, AccountPatch, ProductLoaderPatch, WindowsPatch, SessionWindowPatch
from install import download, install, extract

path = os.path.dirname(sys.argv[0])
patches = [AccountPatch(), ClientAppPatch(), ProductLoaderPatch(), WindowsPatch(), SessionWindowPatch()]


def decompile():
    for p in patches:
        print('DECOMPILING: {}'.format(p.file))
        with open("{}/{}.py".format(path, p.file), "w") as f:
            decompile_file("{}/{}.pyo".format(path, p.file), f)


def patch():
    for p in patches:
        output = []

        print('PATCHING: {}'.format(p.file))

        with open("{}/{}.py".format(path, p.file)) as f:
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

        with open("{}/{}.py".format(path, p.file), "w") as f:
            f.writelines(output)


def recompile():
    for p in patches:
        print('COMPILING: {}'.format(p.file))
        compile('{}/{}.py'.format(path, p.file), '{}/{}.pyo'.format(path, p.file), '-o', doraise=True)


def cleanup():
    for p in patches:
        print('CLEANING: {}'.format(p.file))
        filepath = '{}/{}.py'.format(path, p.file)
        if os.path.isfile(filepath):
            os.remove(filepath)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    download()
    install()
    extract()
    decompile()
    patch()
    recompile()
    cleanup()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
