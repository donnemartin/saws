Release Checklist
=================

A. Review Travis, Codecov, and Gemnasium

B. Run code checks and fix issues

    $ scripts/run_code_checks.sh

C. Verify manual sanity tests prior to release

D. Update version number in `saws/__init__.py`

E. Create `README.rst`

    $ scripts/create_readme_rst.sh

F. Create `CHANGELOG_DRAFT` clean it up, and update CHANGELOG

    $ scripts/create_changelog.sh

Steps G-J can be completed with:

    $ scripts/upload_pypi.sh

G. Register package with PyPi

    $ python setup.py register -r pypi

H. Upload to PyPi

    $ python setup.py sdist upload -r pypi

I. Build Sphinx docs

    $ python setup.py build_sphinx

J. Upload Sphinx docs to PyPi

    $ python setup.py upload_sphinx

K. Review and download newly released package from PyPi

L. Verify manual sanity tests post release
