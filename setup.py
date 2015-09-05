from iawscli.__init__ import __version__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    description='iawscli: an interactive shell for AWS with auto-completion',
    author='Donne Martin',
    url='https://github.com/donnemartin/iawscli',
    download_url='https://github.com/donnemartin/iawscli',
    author_email='donne.martin@gmail.com',
    version=__version__,
    install_requires=[
        'awscli>=1.7.46',
        'click>=4.0',
        'configobj >= 5.0.6',
        'enum34>=1.0.4',
        'fuzzyfinder>=1.0.0',
        'prompt-toolkit==0.46',
        'six>=1.9.0',
        'tabulate>=0.7.5',
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
        'console_scripts': 'iawscli = iawscli.main:cli'
    },
    packages=['iawscli'],
    package_data={'iawscli': ['iawsclirc', 'data/SOURCES.txt']},
    scripts=[],
    name='iawscli',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
