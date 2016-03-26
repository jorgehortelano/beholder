#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import yowsup_ext.beholdernetwork

deps = ['yowsup2==2.4.48', 'beholder-network']

setup(
    name='beholder-network',
    version=yowsup_ext.beholdernetwork.__version__,
    tests_require=[],
    install_requires = deps,
    scripts = ['beholder-network'],
    dependency_links = [
        'https://github.com/tgalal/yowsup/archive/develop.zip#egg=yowsup2-2.4.48',
    ],
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    namespace_packages = ['yowsup_ext', 'yowsup_ext.beholdernetwork', 'yowsup_ext.layers'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
