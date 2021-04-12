#!/usr/bin/env python

import os
import sys

from . import Patcher

from .patches import librarypatch, contentpatch, checksumpatch


def main():
    with Patcher(os.getcwd(), os.getenv('VERSION')) as patcher:
        patcher.download()
        patcher.install()
        patcher.copy()
        patcher.patch(patchers=[librarypatch, contentpatch, checksumpatch])


if __name__ == '__main__':
    sys.exit(main())
