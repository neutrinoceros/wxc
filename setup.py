#!/usr/bin/env python

from distutils.core import setup

project_name = "whych"

setup(
    name=project_name,
    version=__import__(project_name).__version__,
    description="Python Distribution Utilities",
    author="Clément Robert",
    entry_points={"console_scripts": ["whych = whych.__main__:cli"]},
)
