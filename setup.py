#!/usr/bin/env python

from distutils.core import setup

setup(
    name='T5DE',
    version='1.0',
    description='A modified IMVU client that unlocks useful features.',
    packages=['t5de'],
    entry_points={
        'console_scripts': [
            't5de = t5de.__main__:main'
        ]
    }
)
