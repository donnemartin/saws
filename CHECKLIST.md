Release Checklist
=================

A. Run unit tests

    $ tox

B. Run code checks

    $ scripts/run_code_checks.sh

C. Run manual smoke tests on Mac, Ubuntu, Windows*

D. Update and review `CHANGELOG`

    $ scripts/create_changelog.sh

E. Update and review `README.rst`

    $ scripts/create_readme_rst.sh

F. Update and review `Sphinx` docs

    $ python setup.py build_sphinx

G. Push changes

H. Review Travis, Codecov, and Gemnasium

I. Start a new release branch

    $ git flow release start x.y.z

J. Increment the version number in `saws/__init__.py`

    $ scripts/upload_pypi.sh

K. Register package with PyPi

    $ python setup.py register -r pypi

L. Upload to PyPi

    $ python setup.py sdist upload -r pypi

M. Upload Sphinx docs to PyPi

    $ python setup.py upload_sphinx

N. Review newly released package from PyPi

O. Install and run manual smoke tests on Mac, Ubuntu, Windows*

## Smoke Tests

Run the following on Python 2.7 and Python 3.4:

* Craete a new `virtualenv`
* Pip install `SAWS` into new `virtualenv`
* Run `SAWS`
* Empty cache
* Check resource load from cache
* Force refresh of resources
* Toggle toolbar options
* Verify toolbar options are saved across sessions
* Commands
    * Blank
    * aws
    * aws s3api get-bucket-acl --bucket
    * aws ec2 describe-instances --instance-ids
    * aws ecls
    * aws ectagk
    * aws ectagv
    * aws ecstate
    * aws s3 ls s3:
    * aws s3 ls docs
* Run specialized tests based on code changes
