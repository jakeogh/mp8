# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages
from setuptools import setup

import fastentrypoints

if not sys.version_info[0] == 3:
    sys.exit("Python 3 is required. Use: 'python3 setup.py install'")

dependencies = []

config = {
    "version": "0.1",
    "name": "mp8",
    "url": "https://github.com/jakeogh/mp8",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "messagepack str input from terminal",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"mp8": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "mp8=mp8.mp8:main",
            "mpecho=mp8.mp8:main",
        ],
    },
}

setup(**config)
