<!--
SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
SPDX-FileCopyrightText: © 2020 Claudio Jolowicz

SPDX-License-Identifier: MIT
-->

# ⚡ Quickstart Guide

We recommend using [pipx] to manage the requirements, but you can also install
them by replacing [pipx] with `python3 -m pip install --user`. You can [install
pipx] with [pip].

```console
$ python3 -m pip install --user -U pipx
```

The advantage of [pipx] being that the different tools are installed in
separated virtual environments, minimizing the risks of problems.

## Requirements

Python Whiteprint requires [Git], [Poetry] and [Nox].

First [install Git] if it is not already on your computer 😱.

Then install [Poetry]:

```console
$ pipx install poetry
```

Eventually install [Nox] and [inject] the additional dependencies [nox-poetry]
and [rich] into [Nox]'s environment':

```console
$ pipx install nox
$ pipx inject nox nox-poetry rich
```

Note that as [Poetry] and [Nox] are tools that manage environments, they should
should not be included into your own project environment.

## Installing Python Whiterpint

Once the [requirements](#requirements) are satisfied, you can install Python
Whiteprint using once again [pipx].

```console
$ pipx install python-whiteprint
```

🎊 Congratulation 🎊 You are now ready to use Python Whiteprint!

## Creating a project

Generate a Python project:

```console
$ whiteprint init <project_name>
```

And answer the questions and wait for the initialization of your project. Once
finished, a directory named after your project shoud have been created.

### Installing the newly created project

Run the command-line interface from your project source tree:

```console
$ poetry install
$ poetry run <project_slug>
```

### Testing it

Run the full test suite:

```console
$ nox
```

List the available Nox sessions:

```console
$ nox --list-sessions
```

Install the pre-commit hooks:

```console
$ nox -s pre-commit -- install
```

## Continuous Integration

### GitHub

1. Sign up at [GitHub].
2. Generate a new [classic token](https://github.com/settings/tokens) with the
   following permissions:
   - repo (all)
   - workflow
   - write:packages
   - delete:packages
   - delete_repo
3. Generate your project with using the newly created token

   ```console
   $ whiteprint init --github-token <the-github-token>
   ```

#### PyPI

1. Sign up at [PyPI].
2. Go to the Account Settings on PyPI, generate an API token, and copy it.
3. Go to the repository settings on GitHub, and add a secret named `PYPI_TOKEN`
   with the token you just copied.

#### TestPyPI

1. Sign up at [TestPyPI].
2. Go to the Account Settings on TestPyPI, generate an API token, and copy it.
3. Go to the repository settings on GitHub, and add a secret named
   `TEST_PYPI_TOKEN` with the token you just copied.

#### Codecov

1. Sign up at [Codecov].
2. Install their GitHub app.

#### Read the Docs

1. Sign up at [Read the Docs].
2. Import your GitHub repository, using the button _Import a Project_.
3. Install the GitHub webhook,
   using the button _Add integration_
   on the _Integrations_ tab
   in the _Admin_ section of your project
   on Read the Docs.

#### Releasing

Releases are triggered by a version bump on the default branch.
It is recommended to do this in a separate pull request:

1. Switch to a branch.
2. Bump the version using [poetry version].
3. Commit and push to GitHub.
4. Open a pull request.
5. Merge the pull request.

The Release workflow performs the following automated steps:

- Build and upload the package to PyPI.
- Apply a version tag to the repository.
- Publish a GitHub Release.

Release notes are populated with the titles and authors of merged pull requests.
You can group the pull requests into separate sections
by applying labels to them, like this:

<!-- table-release-drafter-sections-begin -->

| Pull Request Label | Section in Release Notes     |
| ------------------ | ---------------------------- |
| `breaking`         | 💥 Breaking Changes          |
| `enhancement`      | 🚀 Features                  |
| `removal`          | 🔥 Removals and Deprecations |
| `bug`              | 🐞 Fixes                     |
| `performance`      | 🐎 Performance               |
| `testing`          | 🚨 Testing                   |
| `ci`               | 👷 Continuous Integration    |
| `documentation`    | 📚 Documentation             |
| `refactoring`      | 🔨 Refactoring               |
| `style`            | 💄 Style                     |
| `dependencies`     | 📦 Dependencies              |

<!-- table-release-drafter-sections-end -->

[git]: https://git-scm.com/
[install git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[codecov]: https://codecov.io/
[cookiecutter]: https://github.com/audreyr/cookiecutter
[github]: https://github.com/
[install-poetry.py]: https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/
[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pipxproject.github.io/pipx/
[install pipx]: https://pypa.github.io/pipx/installation/
[poetry]: https://python-poetry.org/
[poetry version]: https://python-poetry.org/docs/cli/#version
[pyenv]: https://github.com/pyenv/pyenv
[mamba]: https://mamba.readthedocs.io/en/latest/index.html
[pypi]: https://pypi.org/
[read the docs]: https://readthedocs.org/
[testpypi]: https://test.pypi.org/
[rich]: https://rich.readthedocs.io/en/stable/introduction.html
[inject]: https://pypa.github.io/pipx/docs/#pipx-inject
