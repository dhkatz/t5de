#!/usr/bin/env python

import os
import sys

from .patchers import InterfacePatcher, PythonPatcher, ChecksumPatcher
from . import Client


def main():
    with Client(os.getcwd(), os.getenv('IMVU_VERSION')) as patcher:
        patcher.download()
        patcher.install()
        patcher.copy()
        patcher.patch(patchers=[InterfacePatcher, PythonPatcher, ChecksumPatcher])


if __name__ == '__main__':
    sys.exit(main())
