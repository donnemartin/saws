![](http://i.imgur.com/vzC5zmA.gif)

[![Build Status](https://travis-ci.org/donnemartin/saws.svg?branch=master)](https://travis-ci.org/donnemartin/saws) [![Documentation Status](https://readthedocs.org/projects/saws/badge/?version=latest)](http://saws.readthedocs.org/en/latest/?badge=latest) [![Dependency Status](https://gemnasium.com/donnemartin/saws.svg)](https://gemnasium.com/donnemartin/saws) [![Codecov](https://img.shields.io/codecov/c/github/donnemartin/saws.svg)](https://codecov.io/github/donnemartin/saws/saws)

[![PyPI version](https://badge.fury.io/py/saws.svg)](http://badge.fury.io/py/saws) [![PyPI](https://img.shields.io/pypi/pyversions/saws.svg)](https://pypi.python.org/pypi/saws/) [![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

SAWS
====

To view the latest `README`, `docs`, and `code` visit the GitHub repo:

https://github.com/donnemartin/saws

To submit bugs or feature requests, visit the issue tracker:

https://github.com/donnemartin/saws/issues

Changelog
=========

0.4.0 (2015-12-08)
------------------

### Features

* Implemented [#67](https://github.com/donnemartin/saws/issues/67): Add Fish-style auto suggestions.

### Bug Fixes

* Fixed [#71](https://github.com/donnemartin/saws/issues/71): Disable color output for shell commands.
* Fixed [#72](https://github.com/donnemartin/saws/issues/72): Exiting with `F10` does not clear the menu bar.

### Updates

* Updated list of commands.
* Updated repo `README`.
    * Added auto suggestions.
* Fixed [#66](https://github.com/donnemartin/saws/issues/38): Removed `docs/build` from source repo.

0.3.2 (2015-10-16)
------------------

### Features

* Resolved [#38](https://github.com/donnemartin/saws/issues/38): Added `Docker` installation support, by [frosforever](https://github.com/frosforever).
* Resolved [#39](https://github.com/donnemartin/saws/issues/39): Changed completion matching to ignore case.
* Resolved [#40](https://github.com/donnemartin/saws/issues/40): Added `emr --cluster-states` completions.
* Resolved [#52](https://github.com/donnemartin/saws/issues/52) and [#58](https://github.com/donnemartin/saws/issues/58): Updated list of auto-completed commands and subcommands.
* Resolved [#53](https://github.com/donnemartin/saws/issues/53): Moved shortcuts out of `~/.sawsrc` to a new file `~/.saws.shortcuts` to simplify managing shortcuts.

### Bug Fixes

* Fixed [#22](https://github.com/donnemartin/saws/issues/22) and [#26](https://github.com/donnemartin/saws/issues/26):
    * `ordereddict` is now only installed with Python 2.6.
    * `enum34` is now only installed with Python 3.3 and below.
* Fixed [#29](https://github.com/donnemartin/saws/issues/29): `SAWS` is now compatible with  `prompt_toolkit` version 0.52, by [jonathanslenders](https://github.com/jonathanslenders).
* Fixed [#33](https://github.com/donnemartin/saws/issues/29): `SAWS` will no longer exit on keyboard interrupt such as `Ctrl-C`, which can be useful to terminate long-running `aws-cli` commands.
* Fixed [#35](https://github.com/donnemartin/saws/issues/35): Grep now works consistently with shortcuts, by [mlimaloureiro](https://github.com/mlimaloureiro).
* Fixed [#41](https://github.com/donnemartin/saws/issues/41): Blank entry is no longer shown in list of completion if there is no optional value set for a given tag's key.
* Fixed [#60](https://github.com/donnemartin/saws/issues/60): Running an empty command no longer results in a pygmentize syntax error.
* Fixed [#61](https://github.com/donnemartin/saws/issues/61): Refreshing resources multiple times no longer results in an exception.

### Updates

* Added PyPI keywords for easier searching.
* Updated PyPI `README`.
    * Added GitHub repo link, issue tracker, and repo gif.
* Added `INSTALLATION` doc, with the following updates:
    * Added `virtualenv` installation section.
    * Added `Pipsi` installation section [#44](https://github.com/donnemartin/saws/issues/44), by [svieira](https://github.com/svieira).
    * Added `Docker` installation section [#38](https://github.com/donnemartin/saws/issues/38), by [frosforever](https://github.com/frosforever).
* Updated repo `README`.
    * Updated discussion of shortcuts with the new `~/.saws.shortcuts` file.
    * Added Command History section.
    * Updated AWS Credentials and Named Profiles section.
    * Added command to run `SAWS` in the Developer Installation section.
    * Updated Motivation section to include fuzzy shortcut completion, toolbar options, execution and piping of shell commands. and history of commands.
    * Mentioned initial testing of Python 3.5 support.
    * Added install from GitHub source instructions to get the latest dev release
* Updated docs.

0.2.1 (2015-09-23)
------------------

### Bug Fixes

- Fixed [#29](https://github.com/donnemartin/saws/issues/29): Dependency on python-prompt-toolkit > 0.50 breaks saws.

0.2.0 (2015-09-22)
------------------

### Features

- Added support for [#18](https://github.com/donnemartin/saws/issues/18): Multiple syntax highlighting themes.

- Added improved support for [#17](https://github.com/donnemartin/saws/issues/17): Execute shell commands within `SAWS`, including piping.

### Bug Fixes

- Fixed [#21](https://github.com/donnemartin/saws/issues/21): Current command is overwritten on screen when refreshing resources with F5, by [jonathanslenders](https://github.com/jonathanslenders).

### Updates

- Updated `README` installation section with:

    * `Virtualenv` instructions.
    * Details on how to run AWS named profiles/credentials.
    * Supported/tested platforms.

- Updated `README` developer installation section with a new command to build the docs.

- Updated docs.

0.1.1 (2015-09-21)
------------------

### Bug Fixes

- Fixed [#14](https://github.com/donnemartin/saws/issues/14): Fuzzy completions are sometimes showing incorrect
  completions for built-in commands and subcommands.

### Updates

- Updated `README` installation section on how to run `SAWS`.

- Updated docs.

- Updated description, download url, license, and classifiers in
  setup.py.

0.1.0 (2015-09-21)
------------------

- Initial release.
