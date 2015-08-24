#!/usr/bin/env python
import os
from setuptools import setup, find_packages


long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.rst'
    )
).read()


setup(
    name='iawscli',
    author='Donne Martin',
    author_email='donne.martin@gmail.com',
    version='0.1',
    license='LICENSE.txt',
    url='https://github.com/donnemartin/iawscli',
    description='Interactive AWS CLI with auto-completion.',
    long_description=long_description,
    packages=find_packages('.'),
    install_requires = [
        'awscli>=1.7.46',
        'pygments',
        'six>=1.9.0',
        'wcwidth',
    ],
    entry_points='''
        [console_scripts]
        iawscli=iawscli.main:cli
    ''',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Apache 2.0',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
