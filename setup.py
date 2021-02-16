#!/usr/bin/env python

from distutils.core import setup
from os.path import join, dirname

from setuptools import find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='jobs_parser',
    version='1.1.1',
    description='Parser of jobs.by',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Andrei Zaneuski',
    author_email='zanevskiyandrey@gmail.com',
    url='https://github.com/Gliger13/jobs_parser',
    packages=find_packages(),
    python_requires='>=3.8, <4',
    install_requires=requirements,
)
