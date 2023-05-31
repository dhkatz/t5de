#!/usr/bin/env python

import os
import sys

from .patchers import InterfacePatcher, PythonPatcher, ChecksumPatcher
from . import Client


def main():
    IMVU_VERSION = os.getenv('IMVU_VERSION')
    T5DE_VERSION = os.getenv('T5DE_VERSION')

    print('Running T5DE patcher v%s for IMVU v%s' % (T5DE_VERSION, IMVU_VERSION))

    with Client(os.getcwd(), IMVU_VERSION) as patcher:
        patcher.download()
        patcher.install()
        patcher.copy()
        patcher.patch(patchers=[InterfacePatcher, PythonPatcher, ChecksumPatcher], dry_run=False)


if __name__ == '__main__':
    sys.exit(main())
