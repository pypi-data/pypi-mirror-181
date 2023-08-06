#!/usr/bin/env python
"""
ngm
==========
.. code:: shell
  $ ngm list
  $ ngm enable pagespeed
"""
import re

from setuptools import find_packages, setup
import os

_version_re = re.compile(r"__version__\s=\s'(.*)'")

install_requires = [
    'argcomplete', 
    'tabulate', 
    'distro'
]
tests_requires = ["pytest>=4.4.0", "flake8", "pytest-xdist"]

with open("README.md", "r") as fh:
    long_description = fh.read()

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "ngm", "__about__.py"), 'r') as f:
    version = _version_re.search(f.read()).group(1)

setup(
    name="nginx-manager",
    version=version,
    author="Danila Vershinin",
    author_email="info@getpagespeed.com",
    url="https://github.com/GetPageSpeed/ngm",
    description="A CLI tool to manage NGINX configuration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    license="BSD",
    install_requires=install_requires,
    package_data={'ngm': ['*.json']},
    extras_require={
        "tests": install_requires + tests_requires,
        "dev": install_requires + ['pyyaml']
    },
    tests_require=tests_requires,
    include_package_data=True,
    entry_points={"console_scripts": ["ngm = ngm:main"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
