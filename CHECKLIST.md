Release Checklist
=================

A. Install in a new venv and run unit tests

Note, you can't seem to script the virtualenv calls, see:
https://bitbucket.org/dhellmann/virtualenvwrapper/issues/219/cant-deactivate-active-virtualenv-from

    $ deactivate
    $ rmvirtualenv saws
    $ mkvirtualenv saws
    $ pip install -e .
    $ pip install -r requirements-dev.txt
    $ rm -rf .tox && tox

B. Run code checks

    $ scripts/run_code_checks.sh

C. Run manual [smoke tests](#smoke-tests) on Mac, Ubuntu, Windows

D. Update and review `README.rst` and `Sphinx` docs

    $ scripts/update_docs.sh

E. Push changes

F. Review Travis, Codecov, and Gemnasium

G. Start a new release branch

    $ git flow release start x.y.z

H. Increment the version number in `saws/__init__.py`

I. Update and review `CHANGELOG`

    $ scripts/create_changelog.sh

J. Commit the changes

K. Finish the release branch

    $ git flow release finish 'x.y.z'

L. Input a tag

    $ vx.y.z

M. Push tagged release to develop and master

Note: Steps N through R can now be done with a single script:

    $ scripts/release_pypi.sh

N. Set CHANGELOG as `README.md`

    $ scripts/set_changelog_as_readme.sh

O. Register package with PyPi

    $ python setup.py register -r pypi

P. Upload to PyPi

    $ python setup.py sdist upload -r pypi

Q. Upload Sphinx docs to PyPi

    $ python setup.py upload_sphinx

R. Restore `README.md`

    $ scripts/set_changelog_as_readme_undo.sh

S. Review newly released package from PyPi

T. Install in a new venv and run manual [smoke tests](#smoke-tests) on Mac, Ubuntu, Windows

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
* Test the following commands
    * Blank
    * aws
    * aws elb
    * aws s3api get-bucket-acl --bucket
    * aws ec2 describe-instances --instance-ids
    * aws ecls
    * aws ectagk
    * aws ectagv
    * aws ecstate
    * aws s3 ls s3:
    * aws s3 ls docs
* Run targeted tests based on recent code changes
