Contributing
============

Contributions are welcome!

**Please carefully read this page to make the code review process go as smoothly as possible and to maximize the likelihood of your contribution being merged.**

## Bug Reports

For bug reports or requests [submit an issue](https://github.com/donnemartin/saws/issues).

## Pull Requests

The preferred way to contribute is to fork the
[main repository](https://github.com/donnemartin/saws) on GitHub.

1. Fork the [main repository](https://github.com/donnemartin/saws).  Click on the 'Fork' button near the top of the page.  This creates a copy of the code under your account on the GitHub server.

2. Clone this copy to your local disk:

        $ git clone git@github.com:YourLogin/saws.git
        $ cd saws

3. Create a branch to hold your changes and start making changes. Don't work in the `master` branch!

        $ git checkout -b my-feature

4. Work on this copy on your computer using Git to do the version control. When you're done editing, run the following to record your changes in Git:

        $ git add modified_files
        $ git commit

5. Push your changes to GitHub with:

        $ git push -u origin my-feature

6. Finally, go to the web page of your fork of the SAWS repo and click 'Pull Request' to send your changes for review.

### GitHub Pull Requests Docs

If you are not familiar with pull requests, review the [pull request docs](https://help.github.com/articles/using-pull-requests/).

### Code Quality

Ensure your pull request

* Is covered by [unit tests](#unit-tests-and-code-coverage)
* Passes [continuous integration](#continuous-integration)
* Is covered by [documentation](#documentation)

Review the following [style guide](https://google-styleguide.googlecode.com/svn/trunk/pyguide.html).

Run code checks and fix any issues:

    $ cd utility_scripts
    $ ./run_code_checks.sh

### Installation

Refer to the [Installation](https://github.com/donnemartin/saws#installation) and [Developer Installation](https://github.com/donnemartin/saws#developer-installation) sections.
