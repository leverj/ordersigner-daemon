#!/usr/bin/env python
# coding=utf-8
# :bc: Not importing unicode_literals because in Python 2 distutils,
# some values are expected to be byte strings.
from __future__ import absolute_import, division, print_function

from codecs import open

from setuptools import find_packages, setup

# Load long description for PyPI.
with open('README.rst', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    extras_require={
        'dev': [
            'sphinx~=3.2',
            'sphinx-rtd-theme~=0.5',
            'tox~=3.20',
        ]
    },
    author='Phoenix Zerin',
    author_email='phx@phx.ph',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Leverj OrderSigner Daemon',
    install_requires=[
        'twisted~=20.3',

        # ujson v3 dropped support for Python 2.
        # https://github.com/ultrajson/ultrajson/releases/tag/3.0.0
        'ujson~=2.0; python_version < "3"',
        'ujson~=3.2; python_version >= "3"',
    ],
    license='MIT',
    long_description=long_description,
    name='leverj-ordersigner-client',
    packages=find_packages('.', exclude=(
        # For compatibility with Twisted Trial, tests must be in a Python
        # package, but we don't want to include them in dists.
        'tests', 'tests.*',
    )),
    url='https://github.com/leverj/ordersigner-daemon',
    version='1.0rc0',
)
