#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, Command

requirements = []
with open('requirements.txt', 'r') as in_:
    requirements = in_.readlines()

tests_require = ['django']


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='django-measurement',
    version='1.4',
    url='http://github.com/coddingtonbear/django-measurement/',
    description='Convenient fields and classes for handling measurements',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    tests_require=tests_require,
    extras_require={'test': tests_require},
    install_requires=requirements,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=[
        'django_measurement',
    ],
    cmdclass={'test': PyTest},
)
