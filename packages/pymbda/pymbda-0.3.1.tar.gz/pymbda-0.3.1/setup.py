#!/usr/bin/env python

import sys

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    "dacite>=1.6",
    "boto3"
]

# Require python 3.8
if sys.version_info.major != 3 and sys.version_info.minor < 8:
    sys.exit("'pymbda' requires Python >= 3.8!")

setup(
    name="pymbda",
    version="0.3.1",
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/pymbda",
    description="AWS Lambda Tool - Support for building and deploying zip based functions and layers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["AWS", "AWS Lambda", "Lambda", "Serverless"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    license="MIT",
    packages=find_packages(exclude=("test")),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pymbda=pymbda.__main__:main',
        ],
    },
)
