.. figure:: http://i.imgur.com/RGdVOLN.gif
   :alt: 

|PyPI version| |Build Status| |Codecov|

saws
====

Motivation
----------

AWS CLI
~~~~~~~

Although the `AWS CLI <https://github.com/aws/aws-cli>`__ is a great
resource to manage your AWS-powered services, it's **tough to remember
usage** of:

-  50+ top-level commands
-  ~1400 subcommands
-  Countless command-specific options
-  Resources such as instance tags and buckets

Saws: A Supercharged AWS CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Saws`` aims to **supercharge** the AWS CLI with features focusing on:
\* **Improving ease-of-use** \* **Increasing productivity**

Under the hood, ``saws`` is **powered by the AWS CLI** and supports the
**same commands** and **command structure**.

Usage:

::

    aws <command> <subcommand> [parameters] [options]

Features:

-  Auto-completion of:

   -  Commands
   -  Subcommands
   -  Options

-  Auto-completion of resources:

   -  Bucket names
   -  Instance ids
   -  Instance tags
   -  `More coming soon! <(#todo-add-more-resources)>`__

-  Syntax and output highlighting
-  Customizable shortcuts
-  Contextual help

``Saws`` is available for Mac, \*nix, and
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
   -  `Configuring Resource
      Completion <#configuring-resource-completion>`__

-  `Customizable Shortcuts <#customizable-shortcuts>`__
-  `Fuzzy Resource and Shortcut
   Completion <#fuzzy-resource-and-shortcut-completion>`__
-  `Contextual Help <#contextual-help>`__

   -  `Contextual Command Line Help <#contextual-command-line-help>`__
   -  `Contextual Web Docs <#contextual-web-docs>`__

-  `Toolbar Options <#toolbar-options>`__
-  `Windows Support <#windows-support>`__

Installation and Tests
~~~~~~~~~~~~~~~~~~~~~~

-  `Installation <#installation>`__

   -  `Pip Installation <#pip-installation>`__
   -  `Configuring Credentials <#configuring-credentials>`__
   -  `Supported Platforms <#supported-platforms>`__ # `Supported Python
      Versions <#supported-python-versions>`__

-  `Developer Installation <#developer-installation>`__

   -  `Unit Tests <#unit-tests>`__

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

Auto-Completion of Commands, Subcommands, and Options
-----------------------------------------------------

``Saws`` provides smart autocompletion as you type. Entering the
following command will interactively list and auto-complete all
subcommands **specific only to ``ec2``**:

::

    aws ec2

.. figure:: http://i.imgur.com/P2tL9vW.png
   :alt: 

Auto-Completion of AWS Resources
--------------------------------

In addition to the default commands, subcommands, and options the AWS
CLI provides, ``saws`` supports auto-completion of your AWS resources.
Currently, bucket names, instance ids, and instance tags are included,
with additional support for more resources under development.

S3 Buckets
~~~~~~~~~~

Option:

::

    --bucket

Sample Usage:

::

    aws s3api get-bucket-acl --bucket

Note: The example below demonstrates the use of `fuzzy resource
completion <fuzzy-resource-and-shortcutcompletion>`__:

.. figure:: http://i.imgur.com/fNte20g.png
   :alt: 

EC2 Instance Ids
~~~~~~~~~~~~~~~~

Option:

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

Option:

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

.. figure:: http://i.imgur.com/gdEevTp.png
   :alt: 

TODO: Add More Resources
~~~~~~~~~~~~~~~~~~~~~~~~

Feel free to submit an issue or a pull request if you'd like support for
additional resources.

Configuring Resource Completion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can control which resources are loaded on startup and are available
for interactive completion by updating your ``~/.sawsrc`` file:

::

    # AWS resources to refresh
    refresh_instance_ids = True
    refresh_instance_tags = True
    refresh_bucket_names = True

Once initially loaded, resources are cached locally to allow for faster
loading. To refresh the cache, use the ``F5`` key.

Customizable Shortcuts
----------------------

The ``~/.sawsrc`` file contains shortcuts that you can modify. It comes
pre-populated with several `handy
shortcuts <https://github.com/donnemartin/saws/blob/master/saws/sawsrc>`__
out of the box. Below are a few examples.

List all EC2 instances:

::

    aws ec2 ls

List all running EC2 instances:

::

    aws ec2 ls --ec2-state running

.. figure:: http://i.imgur.com/jYFEsoM.png
   :alt: 

List all EC2 instances with a matching tag (supports wildcards ``*``):

::

    aws ec2 ls --ec2-tag-key
    aws ec2 ls --ec2-tag-value

.. figure:: http://i.imgur.com/6lCHfhH.png
   :alt: 

List all DynamoDB tables:

::

    aws dynamodb ls

List all EMR clusters:

::

    aws emr ls

Add/remove/modify shortcuts in your '~/.sawsrc\` file to suit your
needs.

Feel free to submit: \* A pull request if you'd like to share your
shortcuts \* An issue to request additional shortcuts

Fuzzy Resource and Shortcut Completion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To toggle fuzzy completion of AWS resources and shortcuts, use ``F3``
key.

Note: Fuzzy completion currently only works with AWS
`resources <#auto-completion-of-aws-resources>`__ and
`shortcuts <customizable-shortcuts>`__.

.. figure:: http://i.imgur.com/6Z4Zzp4.png
   :alt: 

Contextual Help
---------------

``Saws`` supports contextual command line ``help`` and contextual web
``docs``.

Contextual Command Line Help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``help`` command outputs help within the command line.

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

``Saws`` supports contextual web docs with the ``docs`` command or the
``F1`` key. ``Saws`` will display the web docs specific to the currently
entered command and subcommand.

Usage:

::

    aws <command> <subcommand> docs

.. figure:: http://i.imgur.com/zK4IJYp.png
   :alt: 

Toolbar Options
---------------

``Saws`` supports a number of toolbar options:

-  ``F1`` displays the `contextual web docs <#contextual-web-docs>`__
-  ``F2`` toggles `output syntax
   highlighting <#syntax-and-output-highlighting>`__
-  ``F3`` toggles `fuzzy completion of AWS resources and
   shortcuts <#fuzzy-resource-and-shortcut-completion>`__
-  ``F4`` toggles `completion of shortcuts <#customizable-shortcuts>`__
-  ``F5`` refreshes `resources for
   auto-completion <#auto-completion-of-aws-resources>`__
-  ``F10`` or ``control d`` exits ``saws``

.. figure:: http://i.imgur.com/WzGk9v7.png
   :alt: 

Windows Support
~~~~~~~~~~~~~~~

``Saws`` has been tested on Windows 7 and Windows 10.

On Windows, the ``.sawsrc`` file can be found in ``%userprofile%``. For
example:

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

``Saws`` is hosted on `PyPi <https://pypi.python.org/pypi>`__. The
following command will install ``saws`` along with dependencies such as
the `AWS CLI <https://github.com/aws/aws-cli>`__:

::

    $ pip install saws

Configuring Credentials
~~~~~~~~~~~~~~~~~~~~~~~

`Configure your
credentials <https://github.com/aws/aws-cli#getting-started>`__ with the
AWS CLI:

::

    $ aws configure

For more details on how to install and configure the AWS CLI, refer to
the following
`documentation <http://docs.aws.amazon.com/cli/latest/userguide/installing.html>`__.

Supported Platforms
~~~~~~~~~~~~~~~~~~~

Platforms tested:

-  Mac OS X Yosemite
-  Ubuntu 14.04 LTS
-  Windows 7
-  Windows 10

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~

Python versions tested:

-  Python 2.7
-  Python 3.3
-  Python 3.4

Developer Installation
----------------------

::

    $ git clone https://github.com/donnemartin/wip.git
    $ pip install -e .
    $ pip install -r requirements-dev.txt

Unit Tests
~~~~~~~~~~

After you've completed the `developer
installation <#developer-installation>`__ section, you can run tests
locally.

Run unit tests in your active Python environment:

::

    $ python tests/run_tests.py

Run unit tests with `tox <https://pypi.python.org/pypi/tox>`__ on
multiple versions of Python:

::

    $ tox

Contributing
------------

Bug reports, suggestions, and pull requests are
`welcome <https://github.com/donnemartin/saws/issues>`__!

Credits
-------

-  `AWS CLI <https://github.com/aws/aws-cli>`__ for powering the
   ``saws`` under the hood
-  `Python Prompt
   Toolkit <https://github.com/jonathanslenders/python-prompt-toolkit>`__
   for simplifying the creation of ``saws``

Contact Info
------------

Feel free to contact me to discuss any issues, questions, or comments.

-  Email: donne.martin@gmail.com
-  Twitter: [@donne\_martin](https://twitter.com/donne\_martin)
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

.. |PyPI version| image:: https://badge.fury.io/py/saws.svg
   :target: http://badge.fury.io/py/saws
.. |Build Status| image:: https://travis-ci.org/donnemartin/wip.svg?branch=master
   :target: https://travis-ci.org/donnemartin/saws
.. |Codecov| image:: https://img.shields.io/codecov/c/github/donnemartin/saws.svg
   :target: https://codecov.io/github/donnemartin/saws/saws
