#!/usr/bin/env python

from codecs import open
from setuptools import setup

# Load long description for PyPI.
with open('./README.md', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    author='Phoenix Zerin',
    author_email='phx@phx.ph',
    description='Leverj OrderSigner Daemon',
    license='MIT',
    long_description=long_description,
    name='leverj-ordersigner-daemon',
    url='https://github.com/leverj/ordersigner-daemon',
    version='1.0-pre',
)
