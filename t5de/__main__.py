#!/usr/bin/env python

import os
import sys
import dotenv
import argparse

from .version import __version__
from .patchers import InterfacePatcher, PythonPatcher, ChecksumPatcher
from .diff import InterfaceDiff, PythonDiff
from . import Client


def main():
    parser = argparse.ArgumentParser(prog='t5de', description='The T5DE patcher for IMVU')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run')
    parser.add_argument('--diff', help='Generate a diff between two IMVU versions', const='latest', nargs='?', type=str)
    parser.add_argument('--version', help='The current IMVU version')
    parser.add_argument('--patch', action='store_true', help='Patch the current IMVU version')

    args = parser.parse_args()

    imvu_version = args.version or os.getenv('IMVU_VERSION')
    t5de_version = os.getenv('T5DE_VERSION') or __version__

    if not t5de_version:
        print('T5DE_VERSION environment variable not set')
        return 1

    print('Running T5DE patcher v%s' % t5de_version)

    if args.diff:
        if not imvu_version:
            print('IMVU_VERSION environment variable not set')
            return 1
        version = None if args.diff == 'latest' else args.diff
        with Client(imvu_version) as client:
            client.diff(generators=[InterfaceDiff, PythonDiff], version=version)

    if args.patch:
        if not imvu_version:
            print('IMVU_VERSION environment variable not set')
            return 1
        with Client(imvu_version) as patcher:
            patcher.download()
            patcher.install()
            patcher.copy()
            patcher.patch(patchers=[InterfacePatcher, PythonPatcher, ChecksumPatcher], dry_run=args.dry_run)

    return 0


if __name__ == '__main__':
    dotenv.load_dotenv(override=True)
    sys.exit(main())
