#!/usr/bin/env python

from distutils.core import setup

project_name = "pyw"

setup(
    name=project_name,
    version=__import__(project_name).__version__,
    description="Python Distribution Utilities",
    author="Clément Robert",
    entry_points={"console_scripts": ["pyw=pyw.cli:main"]},
    install_requires=["stdlib_list"],
)
