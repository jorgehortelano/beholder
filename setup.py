#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import yowsup_ext.beholder

deps = ['yowsup2==2.4.48', 'beholder']

setup(
    name='beholder',
    version=yowsup_ext.beholder.__version__,
    tests_require=[],
    install_requires = deps,
    scripts = ['beholder'],
    dependency_links = [
        'https://github.com/tgalal/yowsup/archive/develop.zip#egg=yowsup2-2.4.48',
    ],
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    namespace_packages = ['yowsup_ext', 'yowsup_ext.beholder', 'yowsup_ext.layers'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
