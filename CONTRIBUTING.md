<!--
SPDX-FileCopyrightText: 2023 Romain Brault <mail@romainbrault.com>
SPDX-FileCopyrightText: 2020-2023 Claudio Jolowicz

SPDX-License-Identifier: MIT
-->

# 🛠️ Contributor Guide

Thank you for your interest in improving this project. This project is
open-source under the [MIT license] and welcomes contributions in the form of
bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code]
- [Documentation]
- [Issue Tracker]
- [Code of Conduct]
- [Ideas Discussions]
- [Q&A Discussions]

[MIT License]: https://opensource.org/licenses/MIT
[Source Code]: https://github.com/RomainBrault/python-whiteprint.git
[Documentation]: https://python-whiteprint.readthedocs.io/en/latest/
[Issue Tracker]: https://github.com/RomainBrault/python-whiteprint/issues
[Ideas Discussions]: https://github.com/RomainBrault/python-whiteprint/discussions/categories/ideas
[Q&A Discussions]: https://github.com/RomainBrault/python-whiteprint/discussions/categories/q-a

## How to report a problem

If you have any problem with the project check the [Q&A Discussions] maybe your
question or problem is already answered. Otherwise please open a new discussion!

## How to report an identified bug

Report identified bugs on the [Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Ideas Discussions].

## How to set up your development environment

You need Python 3.8+ and the following tools:

- [Poetry]
- [Nox] with [nox-poetry], [rich] and [beartype] additional dependencies

Once your environment is set-up, install the package with development
requirements:

```console
$ poetry install
```

You can now run an interactive Python session:

```console
$ poetry run python
```

or the Python Whiteprint command-line interface:

```console
$ poetry run whiteprint
```

To avoid prefixing all your commands by `poetry run` you can source a poetry
shell (or activate a virtual environment such as
[Mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html),
[Conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html),
[virtualenv](https://virtualenv.pypa.io/en/latest/) or
[venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)).

For example to activate a virtual environment with poetry run:

```console
$ poetry shell
```

Then you can just run an interactive Python session or the command-line interface:

```console
$ python
```

or

```console
$ {{package_slug}}
```

[poetry]: https://python-poetry.org/
[nox poetry]: https://nox-poetry.readthedocs.io/en/stable/
[rich]: https://rich.readthedocs.io/en/stable/
[beartype]: https://beartype.readthedocs.io/en/latest/
[pipx]: https://pypa.github.io/pipx/

## How to test the project

The test suite is managed by [nox] and [nox-poetry].

Run the full test suite:

```console
$ nox
```

List the available Nox sessions:

```console
$ nox --list-sessions
```

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

```console
$ nox --session=test
```

Unit tests are located in the _tests_ directory,
and are written using the [pytest] testing framework.

[pytest]: https://pytest.readthedocs.io/
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/

## How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the [Documentation] accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you
can install [pre-commit] as a Git hook by running the following command:

```console
$ nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

[pull request]: https://github.com/RomainBrault/python-whiteprint/pulls

<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md
[pre-commit]: https://pre-commit.com/
