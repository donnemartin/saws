![](http://i.imgur.com/vzC5zmA.gif)

[![Build Status](https://travis-ci.org/donnemartin/saws.svg?branch=master)](https://travis-ci.org/donnemartin/saws) [![Documentation Status](https://readthedocs.org/projects/saws/badge/?version=latest)](http://saws.readthedocs.org/en/latest/?badge=latest) [![Dependency Status](https://gemnasium.com/donnemartin/saws.svg)](https://gemnasium.com/donnemartin/saws) [![Codecov](https://img.shields.io/codecov/c/github/donnemartin/saws.svg)](https://codecov.io/github/donnemartin/saws/saws)

[![PyPI version](https://badge.fury.io/py/saws.svg)](http://badge.fury.io/py/saws) [![PyPI](https://img.shields.io/pypi/pyversions/saws.svg)](https://pypi.python.org/pypi/saws/) [![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

SAWS
============

## Motivation

### AWS CLI

Although the [AWS CLI](https://github.com/aws/aws-cli) is a great resource to manage your AWS-powered services, it's **tough to remember usage** of:

* 50+ top-level commands
* ~1400 subcommands
* Countless command-specific options
* Resources such as instance tags and buckets

### SAWS: A Supercharged AWS CLI

`SAWS` aims to **supercharge** the AWS CLI with features focusing on:

* **Improving ease-of-use**
* **Increasing productivity**

Under the hood, `SAWS` is **powered by the AWS CLI** and supports the **same commands** and **command structure**.

`SAWS` and `AWS CLI` Usage:

    aws <command> <subcommand> [parameters] [options]

`SAWS` features:

* Auto-completion of:
    * Commands
    * Subcommands
    * Options
* Auto-completion of resources:
    * Bucket names
    * Instance ids
    * Instance tags
    * [More coming soon!]((#todo-add-more-resources))
* Customizable shortcuts
* Fuzzy completion of resources and shortcuts
* Syntax and output highlighting
* Execution and piping of shell commands
* Command history
* Contextual help
* Toolbar options

`SAWS` is available for Mac, Linux, Unix, and [Windows](#windows-support).

![](http://i.imgur.com/Eo12q9T.png)

## Index

### Features

* [Syntax and Output Highlighting](#syntax-and-output-highlighting)
* [Auto-Completion of Commands, Subcommands, and Options](#auto-completion-of-commands-subcommands-and-options)
* [Auto-Completion of AWS Resources](#auto-completion-of-aws-resources)
    * [S3 Buckets](#s3-buckets)
    * [EC2 Instance Ids](#ec2-instance-ids)
    * [EC2 Instance Tags](#ec2-instance-tags)
    * [TODO: Add More Resources](#todo-add-more-resources)
* [Customizable Shortcuts](#customizable-shortcuts)
* [Fuzzy Resource and Shortcut Completion](#fuzzy-resource-and-shortcut-completion)
* [Executing Shell Commands](#executing-shell-commands)
* [Command History](#command-history)
* [Contextual Help](#contextual-help)
    * [Contextual Command Line Help](#contextual-command-line-help)
    * [Contextual Web Docs](#contextual-web-docs)
* [Toolbar Options](#toolbar-options)
* [Windows Support](#windows-support)

### Installation and Tests

* [Installation](#installation)
    * [Pip Installation](#pip-installation)
    * [Virtual Environment Installation](#virtual-environment-installation)
    * [Pipsi Installation](#pipsi-installation)
    * [AWS Credentials and Named Profiles](#aws-credentials-and-named-profiles)
    * [Supported Python Versions](#supported-python-versions)
    * [Supported Platforms](#supported-platforms)
* [Developer Installation](#developer-installation)
    * [Continuous Integration](#continuous-integration)
    * [Dependencies Management](#dependencies-management)
    * [Unit Tests and Code Coverage](#unit-tests-and-code-coverage)
    * [Documentation](#documentation)

### Misc

* [Contributing](#contributing)
* [Credits](#credits)
* [Contact Info](#contact-info)
* [License](#license)

## Syntax and Output Highlighting

![](http://i.imgur.com/xQDpw70.png)

You can control which theme to load for syntax highlighting by updating your [~/.sawsrc](https://github.com/donnemartin/saws/blob/master/saws/sawsrc) file:

```
# Visual theme. Possible values: manni, igor, xcode, vim, autumn, vs, rrt,
# native, perldoc, borland, tango, emacs, friendly, monokai, paraiso-dark,
# colorful, murphy, bw, pastie, paraiso-light, trac, default, fruity
theme = vim
```

## Auto-Completion of Commands, Subcommands, and Options

`SAWS` provides smart autocompletion as you type.  Entering the following command will interactively list and auto-complete all subcommands **specific only** to `ec2`:

    aws ec2

![](http://i.imgur.com/P2tL9vW.png)

## Auto-Completion of AWS Resources

In addition to the default commands, subcommands, and options the AWS CLI provides, `SAWS` supports auto-completion of your AWS resources.  Currently, bucket names, instance ids, and instance tags are included, with additional support for more resources [under development](#todo-add-more-resources).

### S3 Buckets

Option for `s3api`:

    --bucket

Sample Usage:

    aws s3api get-bucket-acl --bucket

Syntax for `s3`:

    s3://

Sample Usage:

    aws s3 ls s3://

Note:  The example below demonstrates the use of [fuzzy resource completion](fuzzy-resource-and-shortcutcompletion):

![](http://i.imgur.com/39CAS5T.png)

### EC2 Instance Ids

Option for `ec2`:

    --instance-ids

Sample Usage:

    aws ec2 describe-instances --instance-ids
    aws ec2 ls --instance-ids

Note:  The `ls` command demonstrates the use of [customizable shortcuts](#customizable-shortcuts):

![](http://i.imgur.com/jFyCSXl.png)

### EC2 Instance Tags

Option for `ec2`:

    --ec2-tag-key
    --ec2-tag-value

Sample Usage:

    aws ec2 ls --ec2-tag-key
    aws ec2 ls --ec2-tag-value

**Tags support wildcards** with the `*` character.

Note:  `ls`, `--ec2-tag-value`, and `--ec2-tag-key` demonstrate the use of [customizable shortcuts](#customizable-shortcuts):

![](http://i.imgur.com/VIKwG3Z.png)

### TODO: Add More Resources

Feel free to [submit an issue or a pull request](#contributions) if you'd like support for additional resources.

## Customizable Shortcuts

The [~/.sawsrc](https://github.com/donnemartin/saws/blob/master/saws/sawsrc) file contains shortcuts that you can modify.  It comes pre-populated with several [handy shortcuts](https://github.com/donnemartin/saws/blob/master/saws/sawsrc) out of the box.  You can combine shortcuts with [fuzzy completion](#fuzzy-resource-and-shortcut-completion) for even less keystrokes.  Below are a few examples.

List all EC2 instances:

    aws ec2 ls

List all running EC2 instances:

    aws ec2 ls --ec2-state running  # fuzzy shortcut: aws ecstate

![](http://i.imgur.com/jYFEsoM.png)

List all EC2 instances with a matching tag (supports wildcards `*`):

    aws ec2 ls --ec2-tag-key    # fuzzy shortcut: aws ectagk
    aws ec2 ls --ec2-tag-value  # fuzzy shortcut: aws ectagv

![](http://i.imgur.com/PSuwUIw.png)

List EC2 instance with matching id:

    aws ec2 ls --instance-ids  # fuzzy shortcut: aws eclsi

![](http://i.imgur.com/wGcUCsa.png)

List all DynamoDB tables:

    aws dynamodb ls  # fuzzy shortcut: aws dls

List all EMR clusters:

    aws emr ls  # fuzzy shortcut: aws emls

Add/remove/modify shortcuts in your [~/.sawsrc](https://github.com/donnemartin/saws/blob/master/saws/sawsrc) file to suit your needs.

Feel free to submit:

* An issue to request additional shortcuts
* A pull request if you'd like to share your shortcuts (see [contributing guidelines](#contributions))

### Fuzzy Resource and Shortcut Completion

To toggle fuzzy completion of AWS resources and shortcuts, use `F3` key.

Sample fuzzy shortcuts to start and stop EC2 instances:

    aws ecstop
    aws ecstart

Note:  Fuzzy completion currently only works with AWS [resources](#auto-completion-of-aws-resources) and [shortcuts](customizable-shortcuts).

![](http://i.imgur.com/7OvFHCw.png)

### Executing Shell Commands

`SAWS` allows you to execute shell commands from the `saws>` prompt.

![](http://i.imgur.com/FiSn6b2.png)

### Command History

`SAWS` keeps track of commands you enter and stores them in `~/.saws-history`.  Use the up and down arrow keys to cycle through the command history.

![](http://i.imgur.com/z8RrDQB.png)

## Contextual Help

`SAWS` supports contextual command line `help` and contextual web `docs`.

### Contextual Command Line Help

The `help` command is powered by the AWS CLI and outputs help within the command line.

Usage:

    aws <command> <subcommand> help

![](http://i.imgur.com/zSkzt6y.png)

### Contextual Web Docs

Sometimes you're not quite sure what specific command/subcommand/option combination you need to use.  In such cases, browsing through several combinations with the `help` command line is cumbersome versus browsing the online AWS CLI docs through a web browser.

`SAWS` supports contextual web docs with the `docs` command or the `F9` key.  `SAWS` will display the web docs specific to the currently entered command and subcommand.

Usage:

    aws <command> <subcommand> docs

![](http://i.imgur.com/zK4IJYp.png)

## Toolbar Options

`SAWS` supports a number of toolbar options:

* `F2` toggles [output syntax highlighting](#syntax-and-output-highlighting)
* `F3` toggles [fuzzy completion of AWS resources and shortcuts](#fuzzy-resource-and-shortcut-completion)
* `F4` toggles [completion of shortcuts](#customizable-shortcuts)
* `F5` refreshes [resources for auto-completion](#auto-completion-of-aws-resources)
* `F9` displays the [contextual web docs](#contextual-web-docs)
* `F10` or `control d` exits `SAWS`

![](http://i.imgur.com/7vz8OSc.png)

### Windows Support

`SAWS` has been tested on Windows 7 and Windows 10.

On Windows, the [.sawsrc](https://github.com/donnemartin/saws/blob/master/saws/sawsrc) file can be found in `%userprofile%`.  For example:

    C:\Users\dmartin\.sawsrc

Although you can use the standard Windows command prompt, you'll probably have a better experience with either [cmder](https://github.com/cmderdev/cmder) or [conemu](https://github.com/Maximus5/ConEmu).

![](http://i.imgur.com/pUwJWck.png)

## Installation

### Pip Installation

[![PyPI version](https://badge.fury.io/py/saws.svg)](http://badge.fury.io/py/saws) [![PyPI](https://img.shields.io/pypi/pyversions/saws.svg)](https://pypi.python.org/pypi/saws/)

`SAWS` is hosted on [PyPI](https://pypi.python.org/pypi/saws).  The following command will install `SAWS` along with dependencies such as the [AWS CLI](https://github.com/aws/aws-cli):

    $ pip install saws

Once installed, run the following command to start `SAWS`:

    $ saws

### Virtual Environment Installation

It is recommended that you install Python packages in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to avoid potential [issues with dependencies or permissions](https://github.com/donnemartin/saws/issues/15).  If you are a Windows user or if you would like more details on `virtualenv`, check out this [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Install `virtualenv` and `virtualenvwrapper`:

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

1. [Install Pipsi](https://github.com/mitsuhiko/pipsi/blob/master/README.rst)
2. Run `pipsi install saws`
   (or `pipsi install --python=python3 saws` for a Python 3 virtualenv).

### AWS Credentials and Named Profiles

[Configure your credentials](https://github.com/aws/aws-cli#getting-started) with the AWS CLI:

    $ aws configure

If you'd like to use a specific named profile with `SAWS`, run the following commands on OS X, Linux, or Unix:

    $ export AWS_DEFAULT_PROFILE=user1
    $ saws

Or as a one-liner:

    $ AWS_DEFAULT_PROFILE=user1 saws

Windows users can run the following commands:

    > set AWS_DEFAULT_PROFILE=user1
    > saws

Command line options for starting `SAWS` with a specific profile are [under development](https://github.com/donnemartin/saws/issues/16).  For more details on how to install and configure the AWS CLI, refer to the following [documentation](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).

### Supported Python Versions

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* Pypy

Light testing indicates that `SAWS` also seems to be compatible with Python 3.5.

Pypy3 is not supported due to [lack of support](https://github.com/boto/botocore/issues/622) from [boto](https://github.com/boto/boto).

### Supported Platforms

* Mac OS X
    * Tested on OS X 10.10
* Linux, Unix
    * Tested on Ubuntu 14.04 LTS
* Windows
    * Tested on Windows 7 and 10

## Developer Installation

If you're interested in contributing to `SAWS`, run the following commands:

    $ git clone https://github.com/donnemartin/saws.git
    $ pip install -e .
    $ pip install -r requirements-dev.txt
    $ saws

### Continuous Integration

[![Build Status](https://travis-ci.org/donnemartin/saws.svg?branch=master)](https://travis-ci.org/donnemartin/saws)

Continuous integration details are available on [Travis CI](https://travis-ci.org/donnemartin/saws).

### Dependencies Management

[![Dependency Status](https://gemnasium.com/donnemartin/saws.svg)](https://gemnasium.com/donnemartin/saws)

Dependencies management details are available on [Gemnasium](https://gemnasium.com/donnemartin/saws).

### Unit Tests and Code Coverage

[![Codecov](https://img.shields.io/codecov/c/github/donnemartin/saws.svg)](https://codecov.io/github/donnemartin/saws/saws)

![](http://codecov.io/github/donnemartin/saws/branch.svg?branch=master)

Code coverage details are available on [Codecov](https://codecov.io/github/donnemartin/saws/saws).

Run unit tests in your active Python environment:

    $ python tests/run_tests.py

Run unit tests with [tox](https://pypi.python.org/pypi/tox) on multiple Python environments:

    $ tox

### Documentation

[![Documentation Status](https://readthedocs.org/projects/saws/badge/?version=latest)](http://saws.readthedocs.org/en/latest/?badge=latest)

Source code documentation is available on [Readthedocs.org](http://saws.readthedocs.org/en/latest/?badge=latest).

Run the following to build the docs:

    $ scripts/update_docs.sh

## Contributing

Contributions are welcome!

Review the [Contributing Guidelines](https://github.com/donnemartin/saws/blob/master/CONTRIBUTING.md) for details on how to:

* Submit issues
* Submit pull requests

## Credits

* [AWS CLI](https://github.com/aws/aws-cli) by [AWS](https://github.com/aws) for powering `SAWS` under the hood
* [Python Prompt Toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) by [jonathanslenders](https://github.com/jonathanslenders) for simplifying the creation of `SAWS`
* [Wharfee](https://github.com/j-bennet/wharfee) by [j-bennet](https://github.com/j-bennet) for inspiring the creation of `SAWS` and for some handy utility functions

## Contact Info

Feel free to contact me to discuss any issues, questions, or comments.

* Email: [donne.martin@gmail.com](mailto:donne.martin@gmail.com)
* Twitter: [donne_martin](https://twitter.com/donne_martin)
* GitHub: [donnemartin](https://github.com/donnemartin)
* LinkedIn: [donnemartin](https://www.linkedin.com/in/donnemartin)
* Website: [donnemartin.com](http://donnemartin.com)

## License

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
