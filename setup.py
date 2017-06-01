#! /usr/bin/python
import textwrap
import os
from setuptools import setup, find_packages

setup(
    name='huerta',
    version='0.1',
    author='Scott Reynen,Schuyler Duveen',
    author_email='opensource@moveon.org',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/MoveOnOrg/huerta',
    license='MIT',
    description='A Bootstrappy Django theme',
    long_description=textwrap.dedent(open('README.md', 'r').read()),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django'
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ],
)
