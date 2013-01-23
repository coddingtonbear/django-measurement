from setuptools import setup

tests_require=['django']

setup(
    name='django-measurement',
    version='0.9.1',
    url='http://bitbucket.org/latestrevision/django-measurement/',
    description='Convenient fields and classes for handling measurements',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='django_measurement.runtests.runtests',
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
)
