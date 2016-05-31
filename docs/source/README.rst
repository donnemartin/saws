.. figure:: http://i.imgur.com/vzC5zmA.gif
   :alt: 

SAWS
====

|Build Status| |Documentation Status| |Dependency Status| |Codecov|

|PyPI version| |PyPI| |License|

Motivation
----------

AWS CLI
~~~~~~~

Although the `AWS CLI <https://github.com/aws/aws-cli>`__ is a great
resource to manage your AWS-powered services, it's **tough to remember
usage** of:

-  50+ top-level commands
-  1400+ subcommands
-  Countless command-specific options
-  Resources such as instance tags and buckets

SAWS: A Supercharged AWS CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``SAWS`` aims to **supercharge** the AWS CLI with features focusing on:

-  **Improving ease-of-use**
-  **Increasing productivity**

Under the hood, ``SAWS`` is **powered by the AWS CLI** and supports the
**same commands** and **command structure**.

``SAWS`` and ``AWS CLI`` Usage:

::

    aws <command> <subcommand> [parameters] [options]

``SAWS`` features:

-  Auto-completion of:

   -  Commands
   -  Subcommands
   -  Options

-  Auto-completion of resources:

   -  Bucket names
   -  Instance ids
   -  Instance tags
   -  `More coming soon! <#todo-add-more-resources>`__

-  Customizable shortcuts
-  Fuzzy completion of resources and shortcuts
-  Fish-style auto-suggestions
-  Syntax and output highlighting
-  Execution of shell commands
-  Command history
-  Contextual help
-  Toolbar options

``SAWS`` is available for Mac, Linux, Unix, and
`Windows <#windows-support>`__.

.. figure:: http://i.imgur.com/Eo12q9T.png
   :alt: 

Index
-----

Features
~~~~~~~~

-  `Syntax and Output Highlighting <#syntax-and-output-highlighting>`__
-  `Auto-Completion of Commands, Subcommands, and
   Options <#auto-completion-of-commands-subcommands-and-options>`__
-  `Auto-Completion of AWS
   Resources <#auto-completion-of-aws-resources>`__

   -  `S3 Buckets <#s3-buckets>`__
   -  `EC2 Instance Ids <#ec2-instance-ids>`__
   -  `EC2 Instance Tags <#ec2-instance-tags>`__
   -  `TODO: Add More Resources <#todo-add-more-resources>`__

-  `Customizable Shortcuts <#customizable-shortcuts>`__
-  `Fuzzy Resource and Shortcut
   Completion <#fuzzy-resource-and-shortcut-completion>`__
-  `Fish-Style Auto-Suggestions <#fish-style-auto-suggestions>`__
-  `Executing Shell Commands <#executing-shell-commands>`__
-  `Command History <#command-history>`__
-  `Contextual Help <#contextual-help>`__

   -  `Contextual Command Line Help <#contextual-command-line-help>`__
   -  `Contextual Web Docs <#contextual-web-docs>`__

-  `Toolbar Options <#toolbar-options>`__
-  `Windows Support <#windows-support>`__

Installation and Tests
~~~~~~~~~~~~~~~~~~~~~~

-  `Installation <#installation>`__

   -  `Pip Installation <#pip-installation>`__
   -  `Virtual Environment and Docker
      Installation <#virtual-environment-and-docker-installation>`__
   -  `AWS Credentials and Named
      Profiles <#aws-credentials-and-named-profiles>`__
   -  `Supported Python Versions <#supported-python-versions>`__
   -  `Supported Platforms <#supported-platforms>`__

-  `Developer Installation <#developer-installation>`__

   -  `Continuous Integration <#continuous-integration>`__
   -  `Dependencies Management <#dependencies-management>`__
   -  `Unit Tests and Code Coverage <#unit-tests-and-code-coverage>`__
   -  `Documentation <#documentation>`__

Misc
~~~~

-  `Contributing <#contributing>`__
-  `Credits <#credits>`__
-  `Contact Info <#contact-info>`__
-  `License <#license>`__

Syntax and Output Highlighting
------------------------------

.. figure:: http://i.imgur.com/xQDpw70.png
   :alt: 

You can control which theme to load for syntax highlighting by updating
your
`~/.sawsrc <https://github.com/donnemartin/saws/blob/master/saws/sawsrc>`__
file:

::

    # Visual theme. Possible values: manni, igor, xcode, vim, autumn, vs, rrt,
    # native, perldoc, borland, tango, emacs, friendly, monokai, paraiso-dark,
    # colorful, murphy, bw, pastie, paraiso-light, trac, default, fruity
    theme = vim

Auto-Completion of Commands, Subcommands, and Options
-----------------------------------------------------

``SAWS`` provides smart autocompletion as you type. Entering the
following command will interactively list and auto-complete all
subcommands **specific only** to ``ec2``:

::

    aws ec2

.. figure:: http://i.imgur.com/P2tL9vW.png
   :alt: 

Auto-Completion of AWS Resources
--------------------------------

In addition to the default commands, subcommands, and options the AWS
CLI provides, ``SAWS`` supports auto-completion of your AWS resources.
Currently, bucket names, instance ids, and instance tags are included,
with additional support for more resources `under
development <#todo-add-more-resources>`__.

S3 Buckets
~~~~~~~~~~

Option for ``s3api``:

::

    --bucket

Sample Usage:

::

    aws s3api get-bucket-acl --bucket

Syntax for ``s3``:

::

    s3://

Sample Usage:

::

    aws s3 ls s3://

Note: The example below demonstrates the use of `fuzzy resource
completion <fuzzy-resource-and-shortcutcompletion>`__:

.. figure:: http://i.imgur.com/39CAS5T.png
   :alt: 

EC2 Instance Ids
~~~~~~~~~~~~~~~~

Option for ``ec2``:

::

    --instance-ids

Sample Usage:

::

    aws ec2 describe-instances --instance-ids
    aws ec2 ls --instance-ids

Note: The ``ls`` command demonstrates the use of `customizable
shortcuts <#customizable-shortcuts>`__:

.. figure:: http://i.imgur.com/jFyCSXl.png
   :alt: 

EC2 Instance Tags
~~~~~~~~~~~~~~~~~

Option for ``ec2``:

::

    --ec2-tag-key
    --ec2-tag-value

Sample Usage:

::

    aws ec2 ls --ec2-tag-key
    aws ec2 ls --ec2-tag-value

**Tags support wildcards** with the ``*`` character.

Note: ``ls``, ``--ec2-tag-value``, and ``--ec2-tag-key`` demonstrate the
use of `customizable shortcuts <#customizable-shortcuts>`__:

.. figure:: http://i.imgur.com/VIKwG3Z.png
   :alt: 

TODO: Add More Resources
~~~~~~~~~~~~~~~~~~~~~~~~

Feel free to `submit an issue or a pull request <#contributions>`__ if
you'd like support for additional resources.

Customizable Shortcuts
----------------------

The
`~/.saws.shortcuts <https://github.com/donnemartin/saws/blob/master/saws/saws.shortcuts>`__
file contains shortcuts that you can modify. It comes pre-populated with
several `handy
shortcuts <https://github.com/donnemartin/saws/blob/master/saws/saws.shortcuts>`__
out of the box. You can combine shortcuts with `fuzzy
completion <#fuzzy-resource-and-shortcut-completion>`__ for even less
keystrokes. Below are a few examples.

List all EC2 instances:

::

    aws ec2 ls

List all running EC2 instances:

::

    aws ec2 ls --ec2-state running  # fuzzy shortcut: aws ecstate

.. figure:: http://i.imgur.com/jYFEsoM.png
   :alt: 

List all EC2 instances with a matching tag (supports wildcards ``*``):

::

    aws ec2 ls --ec2-tag-key    # fuzzy shortcut: aws ectagk
    aws ec2 ls --ec2-tag-value  # fuzzy shortcut: aws ectagv

.. figure:: http://i.imgur.com/PSuwUIw.png
   :alt: 

List EC2 instance with matching id:

::

    aws ec2 ls --instance-ids  # fuzzy shortcut: aws eclsi

.. figure:: http://i.imgur.com/wGcUCsa.png
   :alt: 

List all DynamoDB tables:

::

    aws dynamodb ls  # fuzzy shortcut: aws dls

List all EMR clusters:

::

    aws emr ls  # fuzzy shortcut: aws emls

Add/remove/modify shortcuts in your
`~/.saws.shortcuts <https://github.com/donnemartin/saws/blob/master/saws/shortcuts>`__
file to suit your needs.

Feel free to submit:

-  An issue to request additional shortcuts
-  A pull request if you'd like to share your shortcuts (see
   `contributing guidelines <#contributions>`__)

Fuzzy Resource and Shortcut Completion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To toggle fuzzy completion of AWS resources and shortcuts, use ``F3``
key.

Sample fuzzy shortcuts to start and stop EC2 instances:

::

    aws ecstop
    aws ecstart

Note: Fuzzy completion currently only works with AWS
`resources <#auto-completion-of-aws-resources>`__ and
`shortcuts <customizable-shortcuts>`__.

.. figure:: http://i.imgur.com/7OvFHCw.png
   :alt: 

Fish-Style Auto-Suggestions
---------------------------

``SAWS`` supports Fish-style auto-suggestions. Use the ``right arrow``
key to complete a suggestion.

.. figure:: http://i.imgur.com/t5200q1.png
   :alt: 

Executing Shell Commands
------------------------

``SAWS`` allows you to execute shell commands from the ``saws>`` prompt.

.. figure:: http://i.imgur.com/FiSn6b2.png
   :alt: 

Command History
---------------

``SAWS`` keeps track of commands you enter and stores them in
``~/.saws-history``. Use the up and down arrow keys to cycle through the
command history.

.. figure:: http://i.imgur.com/z8RrDQB.png
   :alt: 

Contextual Help
---------------

``SAWS`` supports contextual command line ``help`` and contextual web
``docs``.

Contextual Command Line Help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``help`` command is powered by the AWS CLI and outputs help within
the command line.

Usage:

::

    aws <command> <subcommand> help

.. figure:: http://i.imgur.com/zSkzt6y.png
   :alt: 

Contextual Web Docs
~~~~~~~~~~~~~~~~~~~

Sometimes you're not quite sure what specific command/subcommand/option
combination you need to use. In such cases, browsing through several
combinations with the ``help`` command line is cumbersome versus
browsing the online AWS CLI docs through a web browser.

``SAWS`` supports contextual web docs with the ``docs`` command or the
``F9`` key. ``SAWS`` will display the web docs specific to the currently
entered command and subcommand.

Usage:

::

    aws <command> <subcommand> docs

.. figure:: http://i.imgur.com/zK4IJYp.png
   :alt: 

Toolbar Options
---------------

``SAWS`` supports a number of toolbar options:

-  ``F2`` toggles `output syntax
   highlighting <#syntax-and-output-highlighting>`__
-  ``F3`` toggles `fuzzy completion of AWS resources and
   shortcuts <#fuzzy-resource-and-shortcut-completion>`__
-  ``F4`` toggles `completion of shortcuts <#customizable-shortcuts>`__
-  ``F5`` refreshes `resources for
   auto-completion <#auto-completion-of-aws-resources>`__
-  ``F9`` displays the `contextual web docs <#contextual-web-docs>`__
-  ``F10`` or ``control d`` exits ``SAWS``

.. figure:: http://i.imgur.com/7vz8OSc.png
   :alt: 

Windows Support
---------------

``SAWS`` has been tested on Windows 7 and Windows 10.

On Windows, the
`.sawsrc <https://github.com/donnemartin/saws/blob/master/saws/sawsrc>`__
file can be found in ``%userprofile%``. For example:

::

    C:\Users\dmartin\.sawsrc

Although you can use the standard Windows command prompt, you'll
probably have a better experience with either
`cmder <https://github.com/cmderdev/cmder>`__ or
`conemu <https://github.com/Maximus5/ConEmu>`__.

.. figure:: http://i.imgur.com/pUwJWck.png
   :alt: 

Installation
------------

Pip Installation
~~~~~~~~~~~~~~~~

|PyPI version| |PyPI|

``SAWS`` is hosted on `PyPI <https://pypi.python.org/pypi/saws>`__. The
following command will install ``SAWS`` along with dependencies such as
the `AWS CLI <https://github.com/aws/aws-cli>`__:

::

    $ pip install saws

You can also install the latest ``SAWS`` from GitHub source which can
contain changes not yet pushed to PyPI:

::

    $ pip install git+https://github.com/donnemartin/saws.git

If you are not installing in a
`virtualenv <#virtual-environment-and-docker-installation>`__, run with
``sudo``:

::

    $ sudo pip install saws

Once installed, start ``SAWS``:

::

    $ saws

Virtual Environment and Docker Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is recommended that you install Python packages in a
`virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
to avoid potential `issues with dependencies or
permissions <https://github.com/donnemartin/saws/issues/15>`__.

To view ``SAWS`` ``virtualenv`` and `Docker <https://www.docker.com/>`__
installation instructions, click
`here <https://github.com/donnemartin/saws/blob/master/INSTALLATION.md>`__.

Mac OS X 10.11 El Capitan Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a known issue with Apple and its included python package
dependencies (more info at https://github.com/pypa/pip/issues/3165). We
are investigating ways to fix this issue but in the meantime, to install
saws, you can run:

::

    $ sudo pip install saws --upgrade --ignore-installed six

AWS Credentials and Named Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Configure your
credentials <https://github.com/aws/aws-cli#getting-started>`__ with the
AWS CLI:

::

    $ aws configure

If you'd like to use a specific named profile with ``SAWS``, run the
following commands on OS X, Linux, or Unix:

::

    $ export AWS_DEFAULT_PROFILE=user1
    $ saws

Or as a one-liner:

::

    $ AWS_DEFAULT_PROFILE=user1 saws

Windows users can run the following commands:

::

    > set AWS_DEFAULT_PROFILE=user1
    > saws

Command line options for starting ``SAWS`` with a specific profile are
`under development <https://github.com/donnemartin/saws/issues/16>`__.
For more details on how to install and configure the AWS CLI, refer to
the following
`documentation <http://docs.aws.amazon.com/cli/latest/userguide/installing.html>`__.

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~

-  Python 2.6
-  Python 2.7
-  Python 3.3
-  Python 3.4
-  Pypy

Light testing indicates that ``SAWS`` also seems to be compatible with
Python 3.5.

Pypy3 is not supported due to `lack of
support <https://github.com/boto/botocore/issues/622>`__ from
`boto <https://github.com/boto/boto>`__.

Supported Platforms
~~~~~~~~~~~~~~~~~~~

-  Mac OS X

   -  Tested on OS X 10.10

-  Linux, Unix

   -  Tested on Ubuntu 14.04 LTS

-  Windows

   -  Tested on Windows 7 and 10

Developer Installation
----------------------

If you're interested in contributing to ``SAWS``, run the following
commands:

::

    $ git clone https://github.com/donnemartin/saws.git
    $ pip install -e .
    $ pip install -r requirements-dev.txt
    $ saws

Continuous Integration
~~~~~~~~~~~~~~~~~~~~~~

|Build Status|

Continuous integration details are available on `Travis
CI <https://travis-ci.org/donnemartin/saws>`__.

Dependencies Management
~~~~~~~~~~~~~~~~~~~~~~~

|Dependency Status|

Dependencies management details are available on
`Gemnasium <https://gemnasium.com/donnemartin/saws>`__.

Unit Tests and Code Coverage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|Codecov|

.. figure:: http://codecov.io/github/donnemartin/saws/branch.svg?branch=master
   :alt: 

Code coverage details are available on
`Codecov <https://codecov.io/github/donnemartin/saws/saws>`__.

Run unit tests in your active Python environment:

::

    $ python tests/run_tests.py

Run unit tests with `tox <https://pypi.python.org/pypi/tox>`__ on
multiple Python environments:

::

    $ tox

Documentation
~~~~~~~~~~~~~

|Documentation Status|

Source code documentation is available on
`Readthedocs.org <http://saws.readthedocs.org/en/latest/?badge=latest>`__.

Run the following to build the docs:

::

    $ scripts/update_docs.sh

Contributing
------------

Contributions are welcome!

Review the `Contributing
Guidelines <https://github.com/donnemartin/saws/blob/master/CONTRIBUTING.md>`__
for details on how to:

-  Submit issues
-  Submit pull requests

Credits
-------

-  `AWS CLI <https://github.com/aws/aws-cli>`__ by
   `AWS <https://github.com/aws>`__ for powering ``SAWS`` under the hood
-  `Python Prompt
   Toolkit <https://github.com/jonathanslenders/python-prompt-toolkit>`__
   by `jonathanslenders <https://github.com/jonathanslenders>`__ for
   simplifying the creation of ``SAWS``
-  `Wharfee <https://github.com/j-bennet/wharfee>`__ by
   `j-bennet <https://github.com/j-bennet>`__ for inspiring the creation
   of ``SAWS`` and for some handy utility functions

Contact Info
------------

Feel free to contact me to discuss any issues, questions, or comments.

-  Email: donne.martin@gmail.com
-  Twitter: `donne\_martin <https://twitter.com/donne_martin>`__
-  GitHub: `donnemartin <https://github.com/donnemartin>`__
-  LinkedIn: `donnemartin <https://www.linkedin.com/in/donnemartin>`__
-  Website: `donnemartin.com <http://donnemartin.com>`__

License
-------

::

    Copyright 2015 Donne Martin

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

.. |Build Status| image:: https://travis-ci.org/donnemartin/saws.svg?branch=master
   :target: https://travis-ci.org/donnemartin/saws
.. |Documentation Status| image:: https://readthedocs.org/projects/saws/badge/?version=latest
   :target: http://saws.readthedocs.org/en/latest/?badge=latest
.. |Dependency Status| image:: https://gemnasium.com/donnemartin/saws.svg
   :target: https://gemnasium.com/donnemartin/saws
.. |Codecov| image:: https://img.shields.io/codecov/c/github/donnemartin/saws.svg
   :target: https://codecov.io/github/donnemartin/saws/saws
.. |PyPI version| image:: https://badge.fury.io/py/saws.svg
   :target: http://badge.fury.io/py/saws
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/saws.svg
   :target: https://pypi.python.org/pypi/saws/
.. |License| image:: http://img.shields.io/:license-apache-blue.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0.html
