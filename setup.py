#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='bulbascraper',
    version='0.0.1',
    description='Bulbapedia Scraper',
    author='Alexandre Carlton',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
    install_requires=[
        'dataclasses',
        'lxml',
        'mwparserfromhell',
        'requests'
    ]
)
