#!/usr/bin/env python
# coding=utf-8
# :bc: Not importing unicode_literals because in Python 2 distutils,
# some values are expected to be byte strings.
from __future__ import absolute_import, division, print_function

from codecs import open

from setuptools import find_packages, setup

# Load long description for PyPI.
with open("README.rst", "r", "utf-8") as f:
    long_description = f.read()

setup(
    extras_require={
        "dev": [
            "sphinx~=3.2",
            "sphinx-rtd-theme~=0.5",
            "tox~=3.20",
            "nose2~=0.9",
        ]
    },
    author="Phoenix Zerin",
    author_email="phx@phx.ph",
    description="Leverj OrderSigner Daemon",
    install_requires=[
        "ujson~=3.2",
    ],
    license="MIT",
    long_description=long_description,
    name="leverj-ordersigner-client",
    packages=find_packages("."),
    url="https://github.com/leverj/ordersigner-daemon",
    version="1.0rc0",
)
