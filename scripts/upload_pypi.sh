#!/usr/bin/env bash

python setup.py register -r pypi
python setup.py sdist upload -r pypi
python setup.py build_sphinx
python setup.py upload_sphinx