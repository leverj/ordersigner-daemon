#!/usr/bin/env python

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
            'nose2~=0.9',
        ]
    },
    author='Phoenix Zerin',
    author_email='phx@phx.ph',
    description='Leverj OrderSigner Daemon',
    install_requires=[
        'twisted~=20.3',
        'leverj-ordersigner~=0.9',
        'phx-filters~=2.0',
        'ujson~=3.2',
    ],
    license='MIT',
    long_description=long_description,
    name='leverj-ordersigner-daemon',
    packages=find_packages('.'),
    url='https://github.com/leverj/ordersigner-daemon',
    version='1.0rc0',
)
