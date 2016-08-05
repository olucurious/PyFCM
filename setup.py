"""
pyfcm
========

Python client for FCM - Firebase Cloud Messaging (Android & iOS)

Project: https://github.com/olucurious/pyfcm

"""

import os
import sys
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


tests_require = ["mock", "unittest2"]

meta = {}
exec (read('pyfcm/__meta__.py'), meta)

if sys.argv[-1] == 'publish':
    os.system("git tag -a %s -m 'v%s'" % (meta['__version__'], meta['__version__']))
    os.system("python setup.py sdist bdist_wheel upload -r pypi")
    os.system("git push --tags")
    sys.exit()

setup(
    name=meta['__title__'],
    version=meta['__version__'],
    url=meta['__url__'],
    license=meta['__license__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    description=meta['__summary__'],
    long_description=read('README.rst'),
    packages=['pyfcm'],
    install_requires=meta['__install_requires__'],
    tests_require=tests_require,
    test_suite="tests.get_tests",
    keywords='firebase fcm apns ios gcm android push notifications',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
