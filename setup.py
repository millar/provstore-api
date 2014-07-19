#!/usr/bin/env python
from setuptools import setup

setup(name='provstore-api',
    version='0.1',
    description='ProvStore API client',
    author='Sam Millar',
    author_email='sam@millar.io',
    url='https://github.com/millar/provstore-api',
    packages=['provstore'],
    install_requires=[
        'prov>=1.0.0',
        'requests'
    ],
    license="MIT",
    test_suite='provstore.tests',
)
