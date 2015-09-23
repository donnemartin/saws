from saws.__init__ import __version__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    description='SAWS: A Supercharged AWS Command Line Interface (CLI)',
    author='Donne Martin',
    url='https://github.com/donnemartin/saws',
    download_url='https://pypi.python.org/pypi/saws',
    author_email='donne.martin@gmail.com',
    version=__version__,
    license='Apache License 2.0',
    install_requires=[
        'awscli>=1.7.46',
        'click>=4.0',
        'configobj >= 5.0.6',
        'enum34>=1.0.4',
        'fuzzyfinder>=1.0.0',
        'ordereddict>=1.1',
        'prompt-toolkit>=0.46,<=0.50',
        'six>=1.9.0',
        'pygments>=2.0.2'
    ],
    extras_require={
        'testing': [
            'mock>=1.0.1',
            'pytest>=2.7.0',
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': 'saws = saws.main:cli'
    },
    packages=['saws'],
    package_data={'saws': ['sawsrc',
                           'data/SOURCES.txt',
                           'data/RESOURCES_SAMPLE.txt']},
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
