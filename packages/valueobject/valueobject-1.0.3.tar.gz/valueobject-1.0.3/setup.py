#!/usr/bin/env python
# encoding: utf8

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

tests_require=[
    'PythonicTestcase',
],

setup(
    name='valueobject',
    version='1.0.3',
    description='ValueObject is a dict-like object that exposes keys as attributes.',
    long_description=open(path.join(here, 'README.md'), 'rb').read().decode('utf-8'),
    long_description_content_type='text/markdown',
    author='Felix Schwarz, Martin Häcker, Robert Buchholz',
    author_email='rbu@goodpoint.de, spamfaenger@gmx.de',
    license='ISC',
    url='https://github.com/rbu/valueobject',
    packages=find_packages(),
    test_suite="valueobject",
    tests_require=tests_require,
    extras_require = dict(
        testing=tests_require,
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
