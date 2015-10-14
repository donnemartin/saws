from saws.__init__ import __version__
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

install_requires = [
    'awscli>=1.7.46',
    'click>=4.0',
    'configobj>=5.0.6',
    'prompt-toolkit==0.52',
    'six>=1.9.0',
    'pygments>=2.0.2'
]

if sys.version_info < (2, 7):
    # Introduced in Python 2.7
    install_requires.append('ordereddict>=1.1')
if sys.version_info < (3, 4):
    # Backport of Python 3.4 enums to earlier versions
    install_requires.append('enum34>=1.0.4')

setup(
    description='SAWS: A Supercharged AWS Command Line Interface (CLI)',
    author='Donne Martin',
    url='https://github.com/donnemartin/saws',
    download_url='https://pypi.python.org/pypi/saws',
    author_email='donne.martin@gmail.com',
    version=__version__,
    license='Apache License 2.0',
    install_requires=install_requires,
    extras_require={
        'testing': [
            'mock>=1.0.1',
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': 'saws = saws.main:cli'
    },
    packages=find_packages(),
    package_data={'saws': ['sawsrc',
                           'saws.shortcuts',
                           'data/SOURCES.txt',
                           'data/RESOURCES_SAMPLE.txt',
                           'data/OPTIONS.txt']},
    scripts=[],
    name='saws',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
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
