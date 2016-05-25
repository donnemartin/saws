Installation
============

## Pip Installation

[![PyPI version](https://badge.fury.io/py/saws.svg)](http://badge.fury.io/py/saws) [![PyPI](https://img.shields.io/pypi/pyversions/saws.svg)](https://pypi.python.org/pypi/saws/)

`SAWS` is hosted on [PyPI](https://pypi.python.org/pypi/saws).  The following command will install `SAWS` along with dependencies such as the [AWS CLI](https://github.com/aws/aws-cli):

    $ pip install saws

If you are not installing in a [virtualenv](#virtual-environment-installation), run:

    $ sudo pip install saws

Once installed, start `SAWS`:

    $ saws

## Virtual Environment Installation

It is recommended that you install Python packages in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to avoid potential [issues with dependencies or permissions](https://github.com/donnemartin/saws/issues/15).

If you are a Windows user or if you would like more details on `virtualenv`, check out this [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Install `virtualenv` and `virtualenvwrapper`, or check out the [Pipsi Installation](#pipsi-installation) section below:

    pip install virtualenv
    pip install virtualenvwrapper
    export WORKON_HOME=~/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

Create a `SAWS` `virtualenv` and install `SAWS`:

    mkvirtualenv saws
    pip install saws

If you want to activate the `saws` `virtualenv` again later, run:

    workon saws

### Pipsi Installation

[Pipsi](https://github.com/mitsuhiko/pipsi) simplifies the `virtualenv` setup.

Install `pipsi`:

    pip install pipsi

Create a `virtualenv` and install `SAWS`:

    pipsi install saws

For Python 3:

    pipsi install --python=python3 saws

Note:  [Pipsi might not be fully supported on Windows](https://github.com/mitsuhiko/pipsi/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+windows).

## Docker Installation

`SAWS` can be run from docker without additional dependencies. Assuming docker is installed and configured, the docker image can be built by running the following in a directory containing the [Dockerfile](https://github.com/donnemartin/saws/blob/master/Dockerfile):

    docker build -t saws .

`SAWS` can then be run by:

    docker run -it -e AWS_ACCESS_KEY_ID=<key> -e AWS_SECRET_ACCESS_KEY=<secret> -e AWS_DEFAULT_REGION=<region> saws

Or by mounting a local `.aws` configuration directory:

    docker run -it -v path/to/.aws/:/root/.aws:ro saws

## Mac OS X 10.11 El Capitan Users

There is a known issue with Apple and its included python package dependencies (more info at https://github.com/pypa/pip/issues/3165). We are investigating ways to fix this issue but in the meantime, to install saws, you can run:

    $ sudo pip install saws --upgrade --ignore-installed six
