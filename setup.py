#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

requirements = []
with open('requirements.txt', 'r') as in_:
    requirements = in_.readlines()


setup(
    name='django-measurement',
    version='2.0.1',
    url='http://github.com/coddingtonbear/django-measurement/',
    description='Convenient fields and classes for handling measurements',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=[
        'django_measurement',
    ],
)
