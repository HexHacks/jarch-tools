#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='util',
    version='0.1.0',
    description='commonalities',
    author='Jacob Peyron',
    author_email='jacob.peyron@gmail.com',
    packages=find_packages(exclude=('tests', 'docs'))
)

