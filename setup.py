from distutils.core import setup

setup(
    name='django-measurement',
    version='0.4',
    url='http://bitbucket.org/latestrevision/django-measurement/',
    description='Convenient fields and classes for handling measurements',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
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
