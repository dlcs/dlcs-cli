#!/usr/bin/env python3

import os

from setuptools import setup
from setuptools import find_packages


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('src')

# Assignment to placate pyflakes. The actual version is from the exec that
# follows.
__version__ = None

with open(local_file('src/version.py')) as o:
    exec(o.read())

assert __version__ is not None

install_requires = [
    "boto3==1.14.28",
    "botocore==1.17.28",
    "certifi==2019.11.28",
    "chardet==3.0.4",
    "docutils==0.15.2",
    "fire==0.2.1",
    "idna==2.9",
    "jmespath==0.10.0",
    "python-dateutil==2.8.1",
    "requests==2.23.0",
    "s3transfer==0.3.3",
    "six==1.13.0",
    "termcolor==1.1.0",
    "urllib3==1.25.8",
    "attrs==20.3.0"
]

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(local_file('README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dlcs-cli',
    version=__version__,
    description='Command line interface for DLCS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dlcs/dlcs-cli',
    author='Digirati',
    author_email='dlcs@digirati.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(SOURCE),
    package_dir={'': SOURCE},
    install_requires=install_requires,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'dlcs-cli=cli:cli',
        ],
    },
)