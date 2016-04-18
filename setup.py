""" -*- coding: utf-8 -*-
A distutils based setup module.
"""
from distutils.core import setup
setup(
    name='fileasobj',
    packages=['fileasobj'],
    version='2.0.0',
    description='Manage a file as a Python list.',
    author='John Hazelwood',
    author_email='jhazelwo@users.noreply.github.com',
    url='https://github.com/jhazelwo/python-fileasobj',
    download_url='https://github.com/jhazelwo/python-fileasobj/tarball/2.0.0',
    keywords=['python', 'file', 'fileasobj'],
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
