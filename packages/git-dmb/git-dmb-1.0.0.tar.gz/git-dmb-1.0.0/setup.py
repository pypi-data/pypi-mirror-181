#! /usr/bin/env python3
# Copyright (C) 2022 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v3 or later

from setuptools import setup

setup(
    name='git-dmb',
    version='1.0.0',
    license='GPLv3+',
    description='Command-line tool to delete merged Git branches',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Sebastian Pipping',
    author_email='sebastian@pipping.org',
    url='https://github.com/hartwork/git-delete-merged-branches',
    python_requires='>=3.7',
    setup_requires=[
        'setuptools>=38.6.0',  # for long_description_content_type
    ],
    install_requires=[
        'git-delete-merged-branches',
    ],
    packages=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Version Control :: Git',
    ],
)
