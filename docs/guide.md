<!--
SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
SPDX-FileCopyrightText: © 2020 Claudio Jolowicz

SPDX-License-Identifier: MIT
-->

# Project User Guide

:::{warning}
This page is under construction
:::

## Project overview

### Files and directories

This section provides an overview of all the files generated for your project.

Let's start with the directory layout:

:::{list-table} Directories
:widths: auto

- - `src/<package>`
  - Python package
- - `tests`
  - Test suite
- - `docs`
  - Documentation
- - `.github/workflows`
  - [Optional] GitHub Actions workflows

:::

The Python package is located in the `src/<package>` directory. For more
details on these files, refer to the section [The initial
package](the-initial-package). The generated project is a small [Typer] app
printing "Hello, World!".

:::{list-table} Python package
:widths: auto

- - `src/<project>/py.typed`
  - Marker file for [PEP 561][pep 561]
- - `src/<project>/__init__.py`
  - Package initialization
- - `src/<project>/console.py`
  - [Rich] console
- - `src/<project>/hello_world.py`
  - Hello, World! Example
- - `src/<project>/loc.py`
  - Localization
- - `src/<project>/cli/__init__.py`
  - CLI submodule initialization
- - `src/<project>/cli/__main__.py`
  - Command-line top-level code environment
- - `src/<project>/cli/_callback.py`
  - Callback for the [Typer] app
- - `src/<project>/cli/_click_ap.py`
  - Expose a [Click] app from [Typer] for documentation with [sphinx-click]
- - `src/<project>/cli/_loging.py`
  - [Logging] configuration
- - `src/<project>/cli/entrypoint.py`
  - Typer app entrypoint
- - `src/<project>/cli/type.py`
  - Types for the CLI

:::

The test suite is located in the `tests` directory. For more details on these
files, refer to the section [The test suite](the-test-suite).

:::{list-table} Test suite
:widths: auto

- - `tests/__init__.py`
  - Test package initialization
- - `tests/conftest.py`
  - Pytest [fixtures][test fixture]
- - `tests/<project>/test_console.py`
  - Test cases for `str/project/console.py`
- - `tests/<project>/test_version`
  - Test cases for `src/<project>/version.py`
- - `tests/<project>/test_cli/test__click_app.py`
  - Test cases for `src/<project>/clic/_click_app.py`
- - `tests/<project>/test_cli/test_entrypoint.py`
  - Test cases for `src/<project>/clic/entrypoint.py`

:::

The project documentation is written in [Markdown]. The documentation files in
the top-level directory are rendered on [GitHub]:

:::{list-table} Documentation files (top-level)
:widths: auto

- - `README.md`
  - Project description for GitHub and PyPI
- - `CONTRIBUTING.md`
  - Contributor Guide
- - `CODE_OF_CONDUCT.md`
  - Code of Conduct
- - `COPYING`
  - Copying policy (License)

:::

The files in the `docs` directory are built using [Sphinx](documentation) and
[MyST]. The Sphinx documentation is hosted on [Read the
Docs](read-the-docs-integration) if you answered "readthedocs" to the "Where do
you want to host your documentation?" question.

:::{list-table} Documentation files (Sphinx)
:widths: auto

- - `index.md`
  - Main document
- - `contributing.md`
  - Contributor Guide (via include)
- - `codeofconduct.md`
  - Code of Conduct (via include)
- - `reference.md`
  - API reference (auto-generated)
- - `usage.md`
  - Command-line reference (auto-generated)
- - `secuirty.md`
  - Security policy (via include)
- - `dependencies.md`
  - Project dependencies (auto-generated)

:::

The `.github/workflows` directory contains the [GitHub Actions
workflows](github-actions-workflows) if you passed a `--github-token`:

:::{list-table} GitHub Actions workflows
:widths: auto

- - `release.yml`
  - [The Release workflow](the-release-workflow)
- - `tests.yml`
  - [The Tests workflow](the-tests-workflow)
- - `labeler.yml`
  - [The Labeler workflow](the-labeler-workflow)

:::

The project contains many configuration files for developer tools. Most of
these are located in the top-level directory. The table below lists these
files, and links each file to a section with more details.

:::{list-table} Configuration files
:widths: auto

- - `.copier-answers.yml`
  - [Project variables](creating-a-project)
- - `.github/dependabot.yml`
  - Configuration for [Dependabot](dependabot-integration)
- - `.gitattributes`
  - [Git attributes][.gitattributes]
- - `.gitignore`
  - [Git ignore file][.gitignore]
- - `.github/release-drafter.yml`
  - [Optional] Configuration for [Release Drafter](the-release-workflow)
- - `.github/labels.yml`
  - [Optional] Configuration for [GitHub Labeler](the-labeler-workflow)
- - `.pre-commit-config.yaml`
  - Configuration for [pre-commit](linting-with-pre-commit)
- - `.readthedocs.yml`
  - [Optional] Configuration for [Read the Docs](read-the-docs-integration)
- - `docs/conf.py`
  - Configuration for [Sphinx](documentation)
- - `noxfile.py`
  - Configuration for [Nox](using-nox)
- - `pyproject.toml`
  - Configuration for [Poetry](using-poetry),
    [Coverage.py](the-coverage-session),
    [pylint](the-pylint-hook),
    [ruff](the-ruff-hook),
    and [mypy](type-checking-with-mypy)

:::

The `pyproject.toml` file is described in more detail
[below](the-pyproject-toml-file).

[Dependencies](managing-dependencies) are managed by [Poetry] and declared in
the [pyproject.toml](the-pyproject-toml-file) file. The table below lists some
additional files with pinned dependencies. Follow the links for more details on
these.

:::{list-table} Dependency files
:widths: auto

- - `poetry.lock`
  - [Poetry lock file](the-lock-file)
- - `docs/requirements.txt`
  - [Optional] Requirements file for [Read the Docs](read-the-docs-integration)
- - `.github/workflows/constraints.txt`
  - [Optional] Constraints file for [GitHub Actions workflows](workflow-constraints)

:::

(the-initial-package)=

### The initial package

You can find the initial Python package in your generated project
under the `src` directory:

```
src/
└── <package>/
    ├── cli/
        ├── __init__.py
        ├── __main__.py
        ├── _callback.py
        ├── _click_app.py
        ├── _logging.py
        ├── entrypoint.py
        └── type.py
    ├── locale/
        ├── fr_FR/
            └── LC_MESSAGES/
                ├── messages.po
                └── messages.po.license
        ├── base.pot
        └── base.pot.license
    ├── __init__.py
    ├── console.py
    ├── hello_world.py
    ├── loc.py
    ├── py.typed
    └── version.py
```

Some important files are:

<!-- prettier-ignore-start -->

`__init__.py`

: This file declares the directory as a [Python package],
  and contains any package initialization code.

`cli/entrypoint.py`

: The `entrypoint` module defines the entry point for the command-line interface.
  The command-line interface is implemented using the [Typer] library, and
  supports `--help` and `--version` options. When the package is installed, a
  script named `<project>` is placed in the Python installation or virtual
  environment. This allows you to invoke the command-line interface using only
  the project name:

  ```console
  $ poetry run <project>  # during development
  $ <project>             # after installation
  ```

  The command-line interface can also be invoked
  by specifying a Python interpreter and the package name:

  ```console
  $ python -m <package> [<options>]
  ```

`py.typed`

: This is an empty marker file, which declares that your package supports typing and is distributed with its own type information ([PEP 561][pep 561]).
  This allows people using your package to type-check their Python code against
  it.

<!-- prettier-ignore-end -->

(the-test-suite)=

### The test suite

Tests are written using the [pytest] testing framework, the _de facto_ standard
for testing in Python.

The test suite is located in the `tests` directory:

```
tests
├── test_<package>/
    ├── test_cli/
        ├── test__click_app.py
        └── test_entrypoint.py
    ├── test_console.py
    └── test_version.py
├── __init__.py
└── conftest.py
```

The test suite is [declared as a package][pytest layout], and mirrors the
source layout of the package under test.

Initially, the test suite contains a single test case, checking whether the
program exits with a status code of zero. It also provides a [test fixture]
using [click.testing.CliRunner], a helper class for invoking the program from
within tests.

If you do not need a CLI in your project you can remove the two
`tests/test_<package>/test_cli/` and `src/<package>/cli/` directories.

For details on how to run the test suite, refer to the section [The tests
session](the-tests-session).

(documentation)=

### Documentation

The project documentation is written in [Markdown] and processed by the
[Sphinx] documentation engine using the [MyST] extension.

The top-level directory contains several stand-alone documentation files:

<!-- prettier-ignore-start -->

`README.md`

: This file is your main project page and displayed on GitHub and PyPI.

`CONTRIBUTING.md`

: The Contributor Guide explains how other people can contribute to your project.

`CODE_OF_CONDUCT.md`

: The Code of Conduct outlines the behavior expected from participants of your project.
  It is adapted from the [Contributor Covenant], version 2.1.

`COPYING`

: This file contains the text of your project's license.

:::{note}
We follow [Reuse] recommendations. [Do not edit the COPYING
file](https://reuse.software/faq/#edit-license).
:::

The documentation files in the `docs` directory are built using [Sphinx] and
[MyST]:

`index.md`

: This is the main documentation page.
  It includes the project description from `README.md`. This file also defines
  the navigation menu, with links to other documentation pages. The *Changelog*
  menu entry links to the [GitHub Releases][github release] page of your
  project.

`contributing.md`

: This file includes the Contributor Guide from `CONTRIBUTING.md`.

`codeofconduct.md`

: This file includes the Code of Conduct from `CODE_OF_CONDUCT.md`.

`license.md`

: This file includes the license from `LICENSE.md`.

`reference.md`

: The API reference for your project.
  It is generated from docstrings and type annotations in the source code,
  using [Sphinx AutoAPI].

`usage.md`

: The command-line reference for your project.
  It is generated by inspecting the [click] entry-point in the file
  `src/<package>/cli/_click_app.py`, using the [sphinx-click] extension.

The `docs` directory contains two more files:

`conf.py`

: This Python file contains the [Sphinx configuration].

`requirements.txt`

: The requirements file pins the build dependencies for the Sphinx
  documentation. This file is only used on Read the Docs.

<!-- prettier-ignore-end -->

The project documentation is built and hosted on [Read the
Docs](read-the-docs-integration), and uses the [furo] Sphinx theme.

You can also build the documentation locally using Nox, see [The docs
session](the-docs-session).

## Packaging

(the-pyproject-toml-file)=

### The pyproject.toml file

The configuration file for the Python package is located in the root directory
of the project, and named `pyproject.toml`. It uses the [TOML] configuration
file format, and contains two sections---_tables_ in TOML parlance---,
specified in [PEP 517][pep 517] and [518][pep 518]:

- The `build-system` table declares the requirements and the entry point used
  to build a distribution package for the project. This template uses [Poetry]
  as the build system.
- The `tool` table contains sub-tables where tools can store configuration
  under their [PyPI] name.

:::{list-table} Tool configurations in pyproject.toml
:widths: auto

- - `tool.coverage`
  - Configuration for [Coverage.py]
- - `tool.mypy`
  - Configuration for [mypy]
- - `tool.poetry`
  - Configuration for [Poetry]
- - `tool.black`
  - Configuration for [Black]
- - `tool.pytest`
  - Configuration for [Pytest]
- - `tool.ruff`
  - Configuration for [Ruff]
- - `tool.pylint`
  - Configuration for [Pylint]

:::

The `tool.poetry` table contains the metadata for your package, such as its
name, version, and authors, as well as the list of dependencies for the
package. Please refer to the [Poetry documentation][pyproject.toml] for a
detailed description of each configuration key.

(version-constraints)=

### Version constraints

:::{admonition} TL;DR
This project template omits upper bounds from all version constraints.

You are encouraged to manually remove upper bounds for dependencies you add to
your project using Poetry:

1. Replace `^1.2.4` with `>=1.2.4` in `pyproject.toml`
2. Run `poetry lock --no-update` to update `poetry.lock`

:::

[Version constraints][versions and constraints] express which versions of
dependencies are compatible with your project. In the case of core
dependencies, they are also a part of distribution packages, and as such affect
end-users of your package.

:::{note}
Dependencies are Python packages used by your project, and they come in two
types:

- _Core dependencies_ are required by users running your code,
  and typically consist of third-party libraries imported by your package. When
  your package is distributed, the [package metadata] includes these
  dependencies, allowing tools like [pip] to automatically install them
  alongside your package.
- _Development dependencies_ are only required by developers working on your code.
  Examples are applications used to run tests, check code for style and
  correctness, or to build documentation. These dependencies are not a part of
  distribution packages, because users do not require them to run your code.

:::

For every dependency added to your project, Poetry writes a version constraint
to `pyproject.toml`. Dependencies are kept in two TOML tables:

- `tool.poetry.dependencies`---for core dependencies
- `tool.poetry.group.*`---for development dependencies

By default, version constraints added by Poetry have both a lower and an upper
bound:

- The lower bound requires users of your package to have at least the version
  that was current when you added the dependency.
- The upper bound allows users to upgrade to newer releases of dependencies, as
  long as the version number does not indicate a breaking change.

According to the [Semantic Versioning] standard, only major releases may
contain breaking changes, once a project has reached version 1.0.0. A major
release is one that increments the major version (the first component of the
version identifier). An example for such a version constraint would be
`^1.2.4`, which is a Poetry-specific shorthand equivalent to `>= 1.2.4, < 2`.

This project template omits upper bounds from all version constraints, in a
conscious departure from Poetry's defaults. There are two separate reasons for
removing version caps, one principled, the other pragmatic:

1. Version caps lead to problems in the Python ecosystem due to its flat
   dependency management.
2. Version caps lead to frequent merge conflicts between dependency updates.

The first point is treated in detail in the following articles:

- [Should You Use Upper Bound Version Constraints?][schreiner constraints] and [Poetry Versions][schreiner poetry] by Henry Schreiner
- [Semantic Versioning Will Not Save You][schlawack semantic] by Hynek Schlawack
- [Version numbers: how to use them?][gabor version] by Bernát Gábor
- [Why I don't like SemVer anymore][cannon semver] by Brett Cannon

The second point is ultimately due to the fact that every updated version
constraint changes a hashsum in the `poetry.lock` file. This means that PRs
updating version constraints will _always_ conflict with each other.

:::{note}
The problem with merge conflicts is greatly exacerbated by a [Dependabot
issue][dependabot issue 4435]: Dependabot updates version constraints in
`pyproject.toml` even when the version constraint already covered the new
version. This can be avoided using a configuration setting where only the lock
file is ever updated, not the version constraints. Omitting version caps makes
the lockfile-only strategy a viable alternative.
:::

Poetry will still add `^1.2.4`-style version constraints whenever you add a
dependency. You should edit the version constraint in `pyproject.toml`,
replacing `^1.2.4` with `>=1.2.4` to remove the upper bound. Then update the
lock file by invoking `poetry lock --no-update`.

(the-lock-file)=

### The lock file

Poetry records the exact version of each direct and indirect dependency in its
lock file, named `poetry.lock` and located in the root directory of the
project. The lock file does not affect users of the package, because its
contents are not included in distribution packages.

The lock file is useful for a number of reasons:

- It ensures that local checks run in the same environment as on the CI server,
  making the CI predictable and deterministic.
- When collaborating with other developers, it allows everybody to use the same
  development environment.
- When deploying an application, the lock file helps you keep production and
  development environments as similar as possible ([dev-prod parity]).

For these reasons, the lock file should be kept under source control.

### Dependencies

This project template has a core dependency on [Typer], a library based on
[Click] for creating command-line interfaces. The template also comes with
various development dependencies. We also add to the initial dependencies
[Beartype] for runtime type checking and [Rich] for pretty printing.

(using-poetry)=

## Using Poetry

[Poetry] manages packaging and dependencies for Python projects.

(managing-dependencies)=

### Managing dependencies

Use the command [poetry show] to see the full list of direct and indirect
dependencies of your package:

```console
$ poetry show
```

Use the command [poetry add] to add a dependency for your package:

```console
$ poetry add foobar        # for core dependencies
$ poetry add --dev foobar  # for development dependencies
```

:::{important}
It is recommended to remove the upper bound from the version constraint added
by Poetry:

1. Edit `pyproject.toml` to replace `^1.2.3` with `>=1.2.3` in the dependency
   entry
2. Update `poetry.lock` using the command `poetry lock --no-update`

See [Version constraints](version-constraints) for more details.
:::

Use the command [poetry remove] to remove a dependency from your package:

```console
$ poetry remove foobar
```

Use the command [poetry update] to upgrade the dependency to a new release:

```console
$ poetry update foobar
```

:::{note}
Dependencies in Python Whiteprint are managed by
[Dependabot](dependabot-integration). When newer versions of dependencies
become available, Dependabot updates the `poetry.lock` file and submits a pull
request.
:::

### Installing the package for development

Poetry manages a virtual environment for your project, which contains your
package, its core dependencies, and the development dependencies. All
dependencies are kept at the versions specified by the lock file.

:::{note}
A [virtual environment] gives your project an isolated runtime environment,
consisting of a specific Python version and an independent set of installed
Python packages. This way, the dependencies of your current project do not
interfere with the system-wide Python installation, or other projects you're
working on.
:::

You can install your package and its dependencies into Poetry's virtual
environment using the command [poetry install].

```console
$ poetry install
```

This command performs a so-called [editable install] of your package: Instead
of building and installing a distribution package, it creates a special
`.egg-link` file that links to your local source code. This means that code
edits are directly visible in the environment without the need to reinstall
your package.

Installing your package implicitly creates the virtual environment if it does
not exist yet, using the currently active Python interpreter, or the first one
found which satisfies the Python versions supported by your project.

:::{note}
If you already have a [Mamba] virtual environment activated, Poetry will
automatically use it instead of creating a new one.
:::

### Managing environments

Use the command `poetry env info` to show information about the active
environment:

```console
$ poetry env info
```

### Running commands

You can run an interactive Python session inside the active environment using
the command [poetry run]:

```console
$ poetry run python
```

The same command allows you to invoke the command-line interface of your project:

```console
$ poetry run <project>
```

You can also run developer tools, such as [pytest]:

```console
$ poetry run pytest
```

While it is handy to have developer tools available in the Poetry environment,
it is usually recommended to run these using Nox,
as described in the section [Using Nox](using-nox).

### Building and distributing the package

:::{note}
With Python Whiteprint building and distributing your package is taken care of
by [GitHub Actions]. For more information, see the section [The Release
workflow](the-release-workflow).
:::

This section gives a short overview of how you can build and distribute your
package from the command line, using the following Poetry commands:

```console
$ poetry build
$ poetry publish
```

Building the package is done with the [python build] command, which generates
_distribution packages_ in the `dist` directory of your project. These are
compressed archives that an end-user can download and install on their system.
They come in two flavours: source (or _sdist_) archives, and binary packages in
the [wheel] format.

Publishing the package is done with the [python publish] command, which uploads
the distribution packages to your account on [PyPI], the official Python
package registry.

### Installing the package

Once your package is on PyPI, others can install it with [pip], [pipx], or
Poetry:

```console
$ pip install <project>
$ pipx install <project>
$ poetry add <project>
```

While [pip] is the workhorse of the Python packaging ecosystem, you should use
higher-level tools to install your package:

- If the package is an application, install it with [pipx].
- If the package is a library, install it with [poetry add] in other projects.

The primary benefit of these installation methods is that your package is
installed into an isolated environment, without polluting the system
environment, or the environments of other applications. This way, applications
can use specific versions of their direct and indirect dependencies, without
getting in each other's way.

If the other project is not managed by Poetry, use whatever package manager the
other project uses. You can always install your project into a virtual
environment with plain [pip].

(using-nox)=

## Using Nox

[Nox] automates testing in multiple Python environments. Like its older sibling
[tox], Nox makes it easy to run any kind of job in an isolated environment,
with only those dependencies installed that the job needs.

Nox sessions are defined in a Python file named `noxfile.py` and located in the
project directory. They consist of a virtual environment and a set of commands
to run in that environment.

While Poetry environments allow you to interact with your package during
development, Nox environments are used to run developer tools in a reliable and
repeatable way across Python versions.

Most sessions are run with every supported Python version. Other sessions are
only run with the current stable Python version, for example the session used
to build the documentation.

### Running sessions

If you invoke Nox by itself, it will run the full test suite:

```console
$ nox
```

This includes tests, linters, type checks, and more. For the full list, please
refer to the table [below](table-of-nox-sessions).

The list of sessions run by default can be configured by editing
`nox.options.sessions` in `noxfile.py`. Currently the list only excludes the
[docs session](the-docs-session) (which spawns an HTTP server) and the
[coverage session](the-coverage-session) (which is triggered by the [tests
session](the-tests-session)).

You can also run a specific Nox session, using the `--session` option. For
example, build the documentation like this:

```console
$ nox --session=docs
```

Print a list of the available Nox sessions using the `--list-sessions` option:

```console
$ nox --list-sessions
```

Nox creates virtual environments from scratch on each invocation. You can speed
things up by passing the [--reuse-existing-virtualenvs] option, or the
equivalent short option `-R`. For example, the following may be more practical
during development (this will only run tests and type checks, on the current
Python release):

```console
$ nox -Rs tests mypy
```

Many sessions accept additional options after `--` separator. For example, the
following command runs a specific test module:

```console
$ nox --session=tests -- tests/test_main.py
```

### Overview of Nox sessions

(table-of-nox-sessions)=

The following table gives an overview of the available Nox sessions:

:::{list-table} Nox sessions
:header-rows: 1
:widths: auto

- - Session
  - Description
  - Default
- - [coverage](the-coverage-session)
  - Report coverage with [Coverage.py]
  - ✓
- - [docs](the-docs-session)
  - Build and serve [Sphinx] documentation
  - ✓
- - [docs-build](the-docs-build-session)
  - Build [Sphinx] documentation
  - ✓
- - [type-check](the-type-check-session)
  - Type-check with [mypy]
  - ✓
- - [fmt](the-fmt-session)
  - Fromat code with [Ruff] and [Black]
  - ✓
- - [lint](the-lint-session)
  - Lint with [Pylint]
  - ✓
- - [bandit](the-lint-session)
  - Check for code vulnerabilities with [Bandit]
  - ✓
- - [reuse](the-reuse-session)
  - Check licenses with [Reuse]
  - ✓
- - [radon](the-lint-session)
  - Check code complexity with [Radon]
  - ✓
- - [pre-commit](the-pre-commit-session)
  - Run [pre-commit]
  - (✓)
- - [pip-audit](the-pip-audit-session)
  - Scan dependencies with [Pip Audit]
  - (✓)
- - [test](the-tests-session)
  - Run tests with [pytest]
  - (✓)
- - [docs](the-docs-session)
  - Build and serve locally the documentation
  - ✓
- - [docs-build](the-docs-build-session)
  - Build the documentation
  - (✓)
- - [docs-check-links](the-docs-check-links-session)
  - Check the validity of the links in the documentation
  - ✓

:::

(the-docs-session)=

### The docs session

Build the documentation using the Nox session `docs`:

```console
$ nox --session=docs
```

The docs session runs the command `sphinx-autobuild` to generate the HTML
documentation from the Sphinx directory. This tool has several advantages over
`sphinx-build` when you are editing the documentation files:

- It rebuilds the documentation whenever a change is detected.
- It spins up a web server with live reloading.
- It opens the location of the web server in your browser.

Use the `--` separator to pass additional options. For example, to treat
warnings as errors and run in nit-picky mode:

```console
$ nox --session=docs -- -W -n docs docs/_build
```

This Nox session always runs with the current major release of Python.

(the-docs-build-session)=

### The docs-build session

The `docs-build` session runs the command `sphinx-build` to generate the HTML
documentation from the Sphinx directory.

This session is meant to be run as a part of automated checks. Use the
interactive `docs` session instead while you're editing the documentation.

This Nox session always runs with the current major release of Python.

(the-docs-check-links-session)=

### The docs-check-links session

The `docs-check-links` session runs the command `sphinx-build linkcheck` to
check whether all the links in the documentation are valid.

(the-reuse-session)=

### The Reuse session

The `reuse` session runs the command `reuse` to check that all the files in
your project that are commited to the VCS have a valid License file.

(the-fmt-session)=

### The Reuse session

The `fmt` session runs the command `black` and `ruff --fix-only` to format the
code to [Black] code style and fix automatically a maximum of code smells.

(the-type-check-session)=

### The type-check session

[mypy] is the pioneer and _de facto_ reference implementation of static type
checking in Python. Learn more about it in the section [Type-checking with
mypy](type-checking-with-mypy).

Run mypy using Nox:

```console
$ nox --session=mypy
```

You can also run the type checker with a specific Python version. For example,
the following command runs mypy using the current stable release of Python:

```console
$ nox --session=mypy --python=3.11
```

Use the separator `--` to pass additional options and arguments to `mypy`. For
example, the following command type-checks only the `__main__` module:

```console
$ nox --session=mypy -- src/<package>/__main__.py
```

(the-pre-commit-session)=

### The pre-commit session

[pre-commit] is a multi-language linter framework and a Git hook manager. Learn
more about it in the section [Linting with
pre-commit](linting-with-pre-commit).

Run pre-commit from Nox using the `pre-commit` session:

```console
$ nox --session=pre-commit
```

This session always runs with the current stable release of Python.

Use the separator `--` to pass additional options to `pre-commit`. For example,
the following command installs the pre-commit hooks, so they run automatically
on every commit you make:

```console
$ nox --session=pre-commit -- install
```

(the-pip-audit-session)=

### The Pip Audit session

[Pip Audit] checks the dependencies of your project for known security
vulnerabilities, using a curated database of insecure Python packages.

Run [Pip Audit] using the `pip-audit` session:

```console
$ nox --session=pip-audit
```

This session always runs with the current stable release of Python.

(the-tests-session)=

### The test session

Tests are written using the [pytest] testing framework. Learn more about it in
the section [The test suite](the-test-suite).

Run the test suite using the Nox session `test`:

```console
$ nox --session=test
```

The tests session runs the test suite against the installed code. More
specifically, the session builds a wheel from your project and installs it into
the Nox environment, with dependencies pinned as specified by Poetry's lock
file.

You can also run the test suite with a specific Python version. For example,
the following command runs the test suite using the current stable release of
Python:

```console
$ nox --session=test --python=3.11
```

Use the separator `--` to pass additional options to `pytest`. For example, the
following command runs only the test case `test_main_succeeds`:

```console
$ nox --session=test -- -k test_main_succeeds
```

The tests session also installs [pygments], a Python syntax highlighter. It is
used by pytest to highlight code in tracebacks, improving the readability of
test failures.

(the-coverage-session)=

### The coverage session

:::{note}
_Test coverage_ is a measure of the degree to which the source code of your
program is executed while running its test suite.
:::

The coverage session prints a detailed coverage report to the terminal,
combining the coverage data collected during the [tests
session](the-tests-session). If the total coverage is below 100%, the coverage
session fails. Code coverage is measured using [Coverage.py].

The coverage session is triggered by the tests session, and runs after all
other sessions have completed. This allows it to combine the coverage data for
different Python versions.

You can also run the session manually:

```console
$ nox --session=coverage
```

Use the `--` separator to pass arguments to the `coverage` command. For
example, here's how you would generate an HTML report in the `htmlcov`
directory:

```console
$ nox -rs coverage -- html
```

[Coverage.py] is configured in the `pyproject.toml` file, using the
`tool.coverage` table. The configuration informs the tool about your package
name and source tree layout. It also enables branch analysis and the display of
line numbers for missing coverage, and specifies the target coverage
percentage. Coverage is measured for the package as well as [the test suite
itself][batchelder include].

During continuous integration,
coverage data is uploaded to the [Codecov] reporting service.
For details, see the sections about
[Codecov](codecov-integration) and
[The Tests workflow](the-tests-workflow).

(the-lint-session)=

### The lint session

Linting is the automated checking of your source code for programmatic and
stylistic errors. The lint session use [Pylint] to lint the source code in the
`src/`, `tests/` and `docs/` directories. It can also detect code smells, and make
suggestions about how the code could be refactored.

You can run the session manually:

```console
$ nox --session=lint
```

(linting-with-pre-commit)=

## Linting with pre-commit

[pre-commit] is a multi-language linter framework and a Git hook manager. It
allows you to integrate linters and formatters into your Git workflow, even
when written in a language other than Python.

pre-commit is configured using the file `.pre-commit-config.yaml` in the
project directory. Please refer to the [official documentation][pre-commit configuration] for details about the configuration file.

### Running pre-commit from Nox

pre-commit runs in a Nox session every time you invoke `nox`:

```console
$ nox
```

Run the pre-commit session explicitly like this:

```console
$ nox --session=pre-commit
```

The session is described in more detail in the section [The pre-commit
session](the-pre-commit-session).

### Running pre-commit from git

When installed as a [Git hook], pre-commit runs automatically every time you
invoke `git commit`. The commit is aborted if any check fails. When invoked in
this mode, pre-commit only runs on files staged for the commit.

Install pre-commit as a Git hook by running the following command:

```console
$ nox --session=pre-commit -- install
```

### Managing hooks with pre-commit

Hooks in languages other than Python, such as `prettier`, run in isolated
environments managed by pre-commit. To upgrade these hooks, use the
[autoupdate][pre-commit autoupdate] command:

```console
$ nox --session=pre-commit -- autoupdate
```

### Python-language hooks

:::{note}
This section provides some background information about how this project
template integrates pre-commit with Poetry and Nox. You can safely skip this
section.
:::

Python-language hooks in the Python Whiteprint are not managed by pre-commit.
Instead, they are tracked as development dependencies in Poetry, and installed
into the Nox session alongside pre-commit itself. As development dependencies,
they are also present in the Poetry environment.

This approach has some advantages:

- All project dependencies are managed by Poetry.
- Hooks receive automatic upgrades from Dependabot.
- Nox can serve as a single entry point for all checks.
- Additional hook dependencies can be upgraded by a dependency manager. An
  example for this are Flake8 extensions. By contrast, `pre-commit autoupdate`
  does not include additional dependencies.
- Dependencies of dependencies (_subdependencies_) can be locked automatically,
  making checks more repeatable and deterministic.
- Linters and formatters are available in the Poetry environment, which is
  useful for editor integration.

There are also some drawbacks to this technique:

- This is not the officially supported way to integrate pre-commit hooks.
- The hook scripts installed by pre-commit do not activate the virtual
  environment in which pre-commit and the hooks are installed. To work around
  this limitation, the Nox session patches hook scripts on installation.
- Adding a hook is more work, including updating `pyproject.toml` and
  `noxfile.py`, and adding the hook definition to `pre-commit-config.yaml`.

You can always opt out of this integration method, by removing the `repo:
local` section from the configuration file, and adding the official pre-commit
hooks instead. Don't forget to remove the hooks from Poetry's dependencies and
from the Nox session.

:::{note}
Python-language hooks in Python Whiteprint are defined as [system
hooks][pre-commit system hooks]. System hooks don't have their environments
managed by pre-commit; instead, pre-commit assumes that hook dependencies have
already been installed and are available in its environment. The Nox session
for pre-commit takes care of installing the Python hooks alongside pre-commit.

Furthermore, the Python Whiteprint defines Python-language hooks as
[repository-local hooks][pre-commit repository-local hooks]. As such, hook
definitions are not supplied by the hook repositories, but by the project
itself. This makes it possible to override the hook language to `system`, as
explained above.
:::

### Adding an official pre-commit hook

Adding the official pre-commit hook for a linter is straightforward. Often you
can simply copy a configuration snippet from the repository's `README`.
Otherwise, note the hook identifier from the `pre-commit-hooks.yaml` file, and
the git tag for the latest version. Add the following section to your
`pre-commit-config.yaml`, under `repos`:

```yaml
- repo: <hook repository>
  rev: <version tag>
  hooks:
    - id: <hook identifier>
```

While this technique also works for Python-language hooks, it is recommended to
integrate Python hooks with Nox and Poetry, as shown in the next section.

### Adding a Python-language hook

Adding a Python-language hook to your project takes three steps:

- Add the hook as a Poetry development dependency.
- Install the hook in the Nox session for pre-commit.
- Add the hook to `pre-commit-config.yaml`.

For example, consider a linter named `awesome-linter`.

First, use Poetry to add the linter to your development dependencies:

```console
$ poetry add --dev awesome-linter
```

Next, update `noxfile.py` to add the linter to the pre-commit session:

```python
@nox.session(name="pre-commit", ...)
def precommit(session: Session) -> None:
    ...
    session.install(
        "awesome-linter",  # Install awesome-linter
        "black",
        ...
    )
```

Finally, add the hook to `pre-commit-config.yaml` as follows:

- Locate the `pre-commit-hooks.yaml` file in the `awesome-linter` repository.
- Copy the entry for the hook (not just the hook identifier).
- Change `language:` from `python` to `system`.
- Add the hook definition to the `repo: local` section.

Depending on the linter, the hook definition might look somewhat like the
following:

```yaml
repos:
  - repo: local
    hooks:
      # ...
      - id: awesome-linter
        name: Awesome Linter
        entry: awesome-linter
        language: system # was: python
        types: [python]
```

### Running checks on modified files

pre-commit runs checks on the _staged_ contents of files. Any local
modifications are stashed for the duration of the checks. This is motivated by
pre-commit's primary use case, validating changes staged for a commit.

Requiring changes to be staged allows for a nice property: Many pre-commit
hooks support fixing offending lines automatically, for example `black` and
`prettier`. When this happens, your original changes are in the staging area,
while the fixes are in the work tree. You can accept the fixes by staging them
with `git add` before committing again.

If you want to run linters or formatters on modified files, and you do not want
to stage the modifications just yet, you can also invoke the tools via Poetry
instead. For example, use `poetry run ruff <file>` to lint a modified file with
[Ruff].

### Overview of pre-commit hooks

Python Whiteprint comes with a pre-commit configuration consisting,
non-exhaustively, of the following hooks:

:::{list-table} pre-commit hooks
:widths: auto

- - [black]
  - Run the [Black] code formatter
- - [prettier]
  - Run the [Prettier] code formatter
- - [ruff]
  - Run the [Ruff] autofix code formatter
- - [mypy]
  - Run the [Mypy] type checker
- - [Ruff]
  - Run the [Pylint] linter
- - [Bandit]
  - Run the [Bandit] vulnerability analyser
- - [Xenon]
  - Run the [Xenon] code complexity checker

:::

### The Black hook

[Black] is the uncompromising Python code formatter.
One of its greatest features is its lack of configurability.
Blackened code looks the same regardless of the project you're reading.

(the-pylint-hook)=

### The Pylint hook

[Pylint] is a static code analyser (it analyses your code without actually
running it). It checks for errors, enforces a coding standard, looks for code
smells, and can make suggestions about how the code could be refactored.

(the-ruff-hook)=

### The Ruff hook

[Ruff] is an extremely fast Python linter, written in Rust. It is order of
magnitude faster than its cousin [Pylint]. In Python Whiteprint we use [Ruff]
for its autofix feature but prefer the more complete [Pylint] for linting.

### The Prettier hook

[Prettier] is an opinionated code formatter for many languages, including YAML,
Markdown, and JavaScript. Like Black, it has few options, and Python Whiteprint
uses none of them.

### The Bandit hook

[Bandit] is a static code analyser (it analyses your code without actually
running it) designed to find common security issues in Python code.

### Hooks from pre-commit-hooks

The pre-commit configuration also includes several smaller hooks from the
[pre-commit-hooks] repository.

(type-checking-with-mypy)=

## Type-checking with mypy

:::{note}
[Type annotations], first introduced in Python 3.5, are a way to annotate
functions and variables with types. With appropriate tooling, they can make
your programs easier to understand, debug, and maintain.

_Type-checking_ refers to the practice of verifying the type correctness of a
program, using type annotations and type inference. There are two kinds of type
checkers:

- _Static type checkers_ verify the type correctness of your program without
  executing it, using static analysis.
- _Runtime type checkers_ find type errors by instrumenting your code to
  type-check arguments and return values in function calls. This is
  particularly useful during the execution of unit tests.

There is also an increasing number of libraries that leverage type annotations
at runtime. For example, you can use type annotations to generate serialization
schemas or command-line parsers.
:::

[mypy] is the pioneer and _de facto_ reference implementation of static type
checking in Python. Invoke mypy via Nox, as explained in the section [The mypy
session](the-type-check-session).

mypy is configured in the `pyproject.toml` file, using the `tool.mypy` table.
For details about supported configuration options, see the [official
reference][mypy configuration].

Python Whiteprint enables several configuration options which are off by
default.

(external-services)=

## External services

Your GitHub repository can be integrated with several external services for
continuous integration and delivery. This section describes these external
services, what they do, and how to set them up for your repository.

### PyPI

[PyPI] is the official Python Package Index. Uploading your package to PyPI
allows others to download and install it to their system.

Follow these steps to set up PyPI for your repository:

1. Sign up at [PyPI].
2. Go to the Account Settings on PyPI, generate an API token, and copy it.
3. Go to the repository settings on GitHub, and add a secret named `PYPI_TOKEN`
   with the token you just copied.

PyPI is integrated with your repository via the [Release
workflow](the-release-workflow).

### TestPyPI

[TestPyPI] is a test instance of the Python package registry. It allows you to
check your release before uploading it to the real index.

Follow these steps to set up TestPyPI for your repository:

1. Sign up at [TestPyPI].
2. Go to the Account Settings on TestPyPI, generate an API token, and copy it.
3. Go to the repository settings on GitHub, and add a secret named
   `TEST_PYPI_TOKEN` with the token you just copied.

TestPyPI is integrated with your repository via the [Release
workflow](the-release-workflow).

(codecov-integration)=

### Codecov

[Codecov] is a reporting service for code coverage.

Follow these steps to set up Codecov for your repository:

1. Sign up at [Codecov].
2. Install their GitHub app.

The configuration is included in the repository, in the file
[codecov.yml][codecov configuration].

Codecov integrates with your repository via its GitHub app. The [Tests
workflow](the-tests-workflow) uploads the coverage data.

(dependabot-integration)=

### Dependabot

[Dependabot] creates pull requests with automated dependency updates.

Please refer to the [official documentation][dependabot docs] for more details.

The configuration is included in the repository, in the file
[.github/dependabot.yml].

It manages the following dependencies:

:::{list-table}
:header-rows: 1
:widths: auto

- - Type of dependency
  - Managed files
  - See also
- - Python
  - `poetry.lock`
  - [Managing dependencies](managing-dependencies)
- - Python
  - `docs/requirements.txt`
  - [Read the Docs](read-the-docs-integration)
- - Python
  - `.github/workflows/constraints.txt`
  - [Constraints file](workflow-constraints)
- - GitHub Action
  - `.github/workflows/*.yml`
  - [GitHub Actions workflows](github-actions-workflows)

:::

(read-the-docs-integration)=

### Read the Docs

[Read the Docs] automates the building, versioning, and hosting of
documentation.

Follow these steps to set up Read the Docs for your repository:

1. Sign up at [Read the Docs].
2. Import your GitHub repository,
   using the button _Import a Project_.
3. Install the GitHub [webhook][readthedocs webhooks],
   using the button _Add integration_
   on the _Integrations_ tab
   in the _Admin_ section of your project
   on Read the Docs.

Read the Docs automatically starts building your documentation, and will
continue to do so when you push to the default branch or make a release. Your
documentation now has a public URL like this:

> _https://\<project>.readthedocs.io/_

The configuration for Read the Docs is included in the repository, in the file
[.readthedocs.yml]. Python Whiteprint configures Read the Docs to build and
install the package with Poetry, using a so-called [PEP 517][pep 517]-build.

Build dependencies for the documentation are installed using a [requirements
file] located at `docs/requirements.txt`. Read the Docs currently does not
support installing development dependencies using Poetry's lock file. For the
sake of brevity and maintainability, only direct dependencies are included.

:::{note}
The requirements file is managed by [Dependabot](dependabot-integration). When
newer versions of the build dependencies become available, Dependabot updates
the requirements file and submits a pull request. When adding or removing
Sphinx extensions using Poetry, don't forget to update the requirements file as
well.
:::

(github-actions-workflows)=

## GitHub Actions workflows

Python WHiteprint uses [GitHub Actions] to implement continuous integration and
delivery. With GitHub Actions, you define so-called workflows using [YAML]
files located in the `.github/workflows` directory.

A _workflow_ is an automated process consisting of one or many jobs, each of
which executes a series of steps. Workflows are triggered by events, for
example when a commit is pushed or when a release is published. You can learn
more about the workflow language and its supported keywords in the [official
reference][github actions syntax].

:::{note}
Real-time logs for workflow runs are available from the _Actions_ tab in your
GitHub repository.
:::

### Overview of workflows

Python Whiteprint defines the following workflows:

:::{list-table} GitHub Actions workflows
:header-rows: 1
:widths: auto

- - Workflow
  - File
  - Description
  - Trigger
- - [Tests](the-tests-workflow)
  - `tests.yml`
  - Run the test suite with [Nox]
  - Push, PR
- - [Release](the-release-workflow)
  - `release.yml`
  - Upload the package to [PyPI]
  - Push (default branch)
- - [Labeler](the-labeler-workflow)
  - `labeler.yml`
  - Manage GitHub project labels
  - Push (default branch)

:::

### Overview of GitHub Actions

Workflows use the following GitHub Actions:

:::{list-table} GitHub Actions
:widths: auto

- - [actions/cache]
  - Cache dependencies and build outputs
- - [actions/checkout]
  - Check out the Git repository
- - [actions/download-artifact]
  - Download artifacts from workflows
- - [actions/setup-python]
  - Set up workflows with a specific Python version
- - [actions/upload-artifact]
  - Upload artifacts from workflows
- - [codecov/codecov-action]
  - Upload coverage to Codecov
- - [actions/labeler]
  - Manage labels on GitHub as code
- - [pypa/gh-action-pypi-publish]
  - Upload packages to PyPI and TestPyPI
- - [release-drafter/release-drafter]
  - Draft and publish GitHub Releases
- - [salsify/action-detect-and-tag-new-version]
  - Detect and tag new versions in a repository

:::

:::{note}
GitHub Actions used by the workflows are managed by
[Dependabot](dependabot-integration). When newer versions of GitHub Actions
become available, Dependabot updates the workflows that use them and submits a
pull request.
:::

(workflow-constraints)=

### Constraints file

GitHub Actions workflows install the following tools:

- [pip]
- [Poetry]
- [Nox]
- [Nox-Poetry]

These dependencies are pinned using a [constraints file] located in
`.github/workflow/constraints.txt`.

:::{note}
The constraints file is managed by [Dependabot](dependabot-integration). When
newer versions of the tools become available, Dependabot updates the
constraints file and submits a pull request.
:::

(the-tests-workflow)=

### The Tests workflow

The Tests workflow runs checks using Nox. It is triggered on every push to the
repository, and when a pull request is opened or receives new commits.

Each Nox session runs in a separate job, using the current release of Python
and the [latest Ubuntu runner][github actions runners]. Selected Nox sessions
also run on Windows and macOS, and with older Python versions, as shown in the
table below:

The workflow uploads the generated documentation as a [workflow artifact][github actions artifacts].
Building the documentation only serves the purpose of catching issues in pull requests.
Builds on [Read the Docs] happen independently.

The workflow also uploads coverage data to [Codecov] after running tests.
It generates a coverage report in [Cobertura] XML format,
using the [coverage session](the-coverage-session).
The report is uploaded
using the official [Codecov GitHub Action][codecov/codecov-action].

The Tests workflow uses the following GitHub Actions:

- [actions/checkout] for checking out the Git repository
- [actions/setup-python] for setting up the Python interpreter
- [actions/download-artifact] to download the coverage data of each tests
  session
- [actions/cache] for caching pre-commit environments
- [actions/upload-artifact] to upload the generated documentation and the
  coverage data of each tests session
- [codecov/codecov-action] for uploading to [Codecov]

The Tests workflow is defined in `.github/workflows/tests.yml`.

(the-release-workflow)=

### The Release workflow

The Release workflow publishes your package on [PyPI], the Python Package
Index. The workflow also creates a version tag in the GitHub repository, and
publishes a GitHub Release using [Release Drafter]. The workflow is triggered
on every push to the default branch.

Release steps only run if the package version was bumped. If the package
version did not change, the package is instead uploaded to [TestPyPI] as a
prerelease, and only a draft GitHub Release is created. TestPyPI is a test
instance of the Python Package Index.

The Release workflow uses API tokens to access [PyPI] and [TestPyPI]. You can
generate these tokens from your account settings on these services. The tokens
need to be stored as secrets in the repository settings on GitHub:

:::{list-table} Secrets
:widths: auto

- - `PYPI_TOKEN`
  - [PyPI] API token
- - `TEST_PYPI_TOKEN`
  - [TestPyPI] API token

:::

The Release workflow uses the following GitHub Actions:

- [actions/checkout] for checking out the Git repository
- [actions/setup-python] for setting up the Python interpreter
- [salsify/action-detect-and-tag-new-version] for tagging on version bumps
- [pypa/gh-action-pypi-publish] for uploading the package to PyPI or TestPyPI
- [release-drafter/release-drafter] for publishing the GitHub Release

Release notes are populated with the titles and authors of merged pull
requests. You can group the pull requests into separate sections by applying
labels to them, like this:

```{eval-rst}
.. include:: quickstart.md
   :parser: myst_parser.sphinx_
   :start-after: <!-- table-release-drafter-sections-begin -->
   :end-before: <!-- table-release-drafter-sections-end -->
```

The workflow is defined in `.github/workflows/release.yml`. The Release Drafter
configuration is located in `.github/release-drafter.yml`.

(the-labeler-workflow)=

### The Labeler workflow

The Labeler workflow manages the labels used in GitHub issues and pull requests
based on a description file `.github/labels.yaml`. In this file each label is
described with
a `name`,
a `description`
and a `color`.
The workflow is triggered on every push to the default branch.

The workflow creates or updates project labels if they are missing or different
compared to the `labels.yml` file content.

The workflow does not delete labels already configured in the GitHub UI and not
in the `labels.yml` file. You can change this behavior and add ignore patterns
in the settings of the workflow (see [GitHub Labeler] documentation).

The Labeler workflow uses the following GitHub Actions:

- [actions/checkout] for checking out the Git repository
- [actions/labeler] for updating the GitHub project labels

The workflow is defined in `.github/workflows/labeler.yml`. The GitHub Labeler
configuration is located in `.github/labels.yml`.

(tutorials)=

## Tutorials

First, make sure you have all the [requirements](installation) installed.

(how-to-test-your-project)=

### How to test your project

Run the test suite using [Nox](using-Nox):

```console
$ nox
```

### How to run your code

First, install the project and its dependencies to the Poetry environment:

```console
$ poetry install
```

Run an interactive session in the environment:

```console
$ poetry run python
```

Invoke the command-line interface of your package:

```console
$ poetry run <project>
```

## The Hypermodern Python blog

The project setup is heavily inspired by the [Hypermodern Python] article
series:

- [Chapter 1: Setup][hypermodern python chapter 1]
- [Chapter 2: Testing][hypermodern python chapter 2]
- [Chapter 3: Linting][hypermodern python chapter 3]
- [Chapter 4: Typing][hypermodern python chapter 4]
- [Chapter 5: Documentation][hypermodern python chapter 5]
- [Chapter 6: CI/CD][hypermodern python chapter 6]

You can also read the articles on [this blog][hypermodern python blog].

[pylint]: https://pylint.readthedocs.io/en/latest/
[ruff]: https://beta.ruff.rs/docs/
[Beartype]: https://beartype.readthedocs.io/en/latest/
[sphinx autoapi]: https://sphinx-autoapi.readthedocs.io/en/latest/
[reuse]: https://reuse.software
[logging]: https://docs.python.org/3/library/logging.html
[Typer]: https://typer.tiangolo.com/
[github token]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
[rich]: https://rich.readthedocs.io/en/stable/introduction.html
[mamba user guide]: https://mamba.readthedocs.io/en/latest/user_guide/mamba.html
[python whiteprint]: https://github.com/RomainBrault/python-whiteprint
[--reuse-existing-virtualenvs]: https://nox.thea.codes/en/stable/usage.html#re-using-virtualenvs
[.gitattributes]: https://git-scm.com/book/en/Customizing-Git-Git-Attributes
[.github/dependabot.yml]: https://docs.github.com/en/github/administering-a-repository/configuration-options-for-dependency-updates
[.gitignore]: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_ignoring
[.readthedocs.yml]: https://docs.readthedocs.io/en/stable/config-file/v2.html
[__main__]: https://docs.python.org/3/library/__main__.html
[abstract syntax tree]: https://docs.python.org/3/library/ast.html
[actions/cache]: https://github.com/actions/cache
[actions/checkout]: https://github.com/actions/checkout
[actions/download-artifact]: https://github.com/actions/download-artifact
[actions/setup-python]: https://github.com/actions/setup-python
[actions/upload-artifact]: https://github.com/actions/upload-artifact
[autodoc]: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
[bandit codes]: https://bandit.readthedocs.io/en/latest/plugins/index.html#complete-test-plugin-listing
[bandit]: https://github.com/PyCQA/bandit
[bash]: https://www.gnu.org/software/bash/
[batchelder include]: https://nedbatchelder.com/blog/202008/you_should_include_your_tests_in_coverage.html
[black]: https://github.com/psf/black
[semantic versioning]: https://semver.org/
[cannon semver]: https://snarky.ca/why-i-dont-like-semver/
[check-added-large-files]: https://github.com/pre-commit/pre-commit-hooks#check-added-large-files
[check-toml]: https://github.com/pre-commit/pre-commit-hooks#check-toml
[check-yaml]: https://github.com/pre-commit/pre-commit-hooks#check-yaml
[click.testing.clirunner]: https://click.palletsprojects.com/en/7.x/testing/
[click]: https://click.palletsprojects.com/
[cobertura]: https://cobertura.github.io/cobertura/
[codecov configuration]: https://docs.codecov.io/docs/codecov-yaml
[codecov/codecov-action]: https://github.com/codecov/codecov-action
[codecov]: https://codecov.io/
[constraints file]: https://pip.pypa.io/en/stable/user_guide/#constraints-files
[contributor covenant]: https://www.contributor-covenant.org
[copier]: https://github.com/copier-org/copier
[coverage.py]: https://coverage.readthedocs.io/
[crazy-max/ghaction-github-labeler]: https://github.com/crazy-max/ghaction-github-labeler
[cupper]: https://github.com/senseyeio/cupper
[curl]: https://curl.haxx.se
[cyclomatic complexity]: https://en.wikipedia.org/wiki/Cyclomatic_complexity
[dependabot docs]: https://docs.github.com/en/github/administering-a-repository/keeping-your-dependencies-updated-automatically
[dependabot issue 4435]: https://github.com/dependabot/dependabot-core/issues/4435
[dependabot]: https://dependabot.com/
[dev-prod parity]: https://12factor.net/dev-prod-parity
[editable install]: https://pip.pypa.io/en/stable/cli/pip_install/#install-editable
[end-of-file-fixer]: https://github.com/pre-commit/pre-commit-hooks#end-of-file-fixer
[furo]: https://pradyunsg.me/furo/
[future imports]: https://docs.python.org/3/library/__future__.html
[gabor version]: https://bernat.tech/posts/version-numbers/
[git hook]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
[git]: https://www.git-scm.com
[github actions artifacts]: https://help.github.com/en/actions/configuring-and-managing-workflows/persisting-workflow-data-using-artifacts
[github actions runners]: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/virtual-environments-for-github-hosted-runners#supported-runners-and-hardware-resources
[github actions syntax]: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions
[github actions]: https://github.com/features/actions
[github labeler]: https://github.com/marketplace/actions/github-labeler
[github release]: https://help.github.com/en/github/administering-a-repository/about-releases
[github renaming]: https://github.com/github/renaming
[github]: https://github.com/
[google docstring style]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[hypermodern python blog]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
[hypermodern python chapter 1]: https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769
[hypermodern python chapter 2]: https://medium.com/@cjolowicz/hypermodern-python-2-testing-ae907a920260
[hypermodern python chapter 3]: https://medium.com/@cjolowicz/hypermodern-python-3-linting-e2f15708da80
[hypermodern python chapter 4]: https://medium.com/@cjolowicz/hypermodern-python-4-typing-31bcf12314ff
[hypermodern python chapter 5]: https://medium.com/@cjolowicz/hypermodern-python-5-documentation-13219991028c
[hypermodern python chapter 6]: https://medium.com/@cjolowicz/hypermodern-python-6-ci-cd-b233accfa2f6
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[hypermodern python]: https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769
[import hook]: https://docs.python.org/3/reference/import.html#import-hooks
[install-poetry.py]: https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py
[isort black profile]: https://pycqa.github.io/isort/docs/configuration/black_compatibility.html
[isort force_single_line]: https://pycqa.github.io/isort/docs/configuration/options.html#force-single-line
[isort lines_after_imports]: https://pycqa.github.io/isort/docs/configuration/options.html#lines-after-imports
[isort]: https://pycqa.github.io/isort/
[jinja]: https://palletsprojects.com/p/jinja/
[json]: https://www.json.org/
[markdown]: https://spec.commonmark.org/current/
[mccabe]: https://github.com/PyCQA/mccabe
[mit license]: https://opensource.org/licenses/MIT
[mypy configuration]: https://mypy.readthedocs.io/en/stable/config_file.html
[mypy]: http://mypy-lang.org/
[myst]: https://myst-parser.readthedocs.io/
[napoleon]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
[nox-poetry]: https://nox-poetry.readthedocs.io/
[nox]: https://nox.thea.codes/
[package metadata]: https://packaging.python.org/en/latest/specifications/core-metadata/
[pep 257]: http://www.python.org/dev/peps/pep-0257/
[pep 440]: https://www.python.org/dev/peps/pep-0440/
[pep 517]: https://www.python.org/dev/peps/pep-0517/
[pep 518]: https://www.python.org/dev/peps/pep-0518/
[pep 561]: https://www.python.org/dev/peps/pep-0561/
[pep 8]: http://www.python.org/dev/peps/pep-0008/
[pep8-naming codes]: https://github.com/pycqa/pep8-naming#pep-8-naming-conventions
[pep8-naming]: https://github.com/pycqa/pep8-naming
[pip install]: https://pip.pypa.io/en/stable/reference/pip_install/
[pip]: https://pip.pypa.io/
[pipx]: https://pipxproject.github.io/pipx/
[poetry add]: https://python-poetry.org/docs/cli/#add
[poetry env]: https://python-poetry.org/docs/managing-environments/
[poetry export]: https://python-poetry.org/docs/cli/#export
[poetry install]: https://python-poetry.org/docs/cli/#install
[poetry remove]: https://python-poetry.org/docs/cli/#remove
[poetry run]: https://python-poetry.org/docs/cli/#run
[poetry show]: https://python-poetry.org/docs/cli/#show
[poetry update]: https://python-poetry.org/docs/cli/#update
[poetry version]: https://python-poetry.org/docs/cli/#version
[poetry]: https://python-poetry.org/
[pre-commit autoupdate]: https://pre-commit.com/#pre-commit-autoupdate
[pre-commit configuration]: https://pre-commit.com/#adding-pre-commit-plugins-to-your-project
[pre-commit repository-local hooks]: https://pre-commit.com/#repository-local-hooks
[pre-commit system hooks]: https://pre-commit.com/#system
[pre-commit-hooks]: https://github.com/pre-commit/pre-commit-hooks
[pre-commit]: https://pre-commit.com/
[prettier]: https://prettier.io/
[pycodestyle codes]: https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
[pycodestyle]: https://pycodestyle.pycqa.org/en/latest/
[pydocstyle codes]: http://www.pydocstyle.org/en/stable/error_codes.html
[pydocstyle]: http://www.pydocstyle.org/
[pyenv wiki]: https://github.com/pyenv/pyenv/wiki/Common-build-problems
[pyenv]: https://github.com/pyenv/pyenv
[pygments]: https://pygments.org/
[pypa/gh-action-pypi-publish]: https://github.com/pypa/gh-action-pypi-publish
[pypi]: https://pypi.org/
[pyproject.toml]: https://python-poetry.org/docs/pyproject/
[pytest layout]: https://docs.pytest.org/en/latest/explanation/goodpractices.html#choosing-a-test-layout-import-rules
[pytest]: https://docs.pytest.org/en/latest/
[python build]: https://python-poetry.org/docs/cli/#build
[python package]: https://docs.python.org/3/tutorial/modules.html#packages
[python publish]: https://python-poetry.org/docs/cli/#publish
[python website]: https://www.python.org/
[pyupgrade]: https://github.com/asottile/pyupgrade
[read the docs]: https://readthedocs.org/
[readthedocs webhooks]: https://docs.readthedocs.io/en/stable/webhooks.html
[relative imports]: https://docs.python.org/3/reference/import.html#package-relative-imports
[release drafter]: https://github.com/release-drafter/release-drafter
[release-drafter/release-drafter]: https://github.com/release-drafter/release-drafter
[requirements file]: https://pip.readthedocs.io/en/stable/user_guide/#requirements-files
[restructuredtext]: https://docutils.sourceforge.io/rst.html
[pip audit]: https://github.com/pypa/pip-audit
[salsify/action-detect-and-tag-new-version]: https://github.com/salsify/action-detect-and-tag-new-version
[schlawack semantic]: https://hynek.me/articles/semver-will-not-save-you/
[schreiner constraints]: https://iscinumpy.dev/post/bound-version-constraints/
[schreiner poetry]: https://iscinumpy.dev/post/poetry-versions/
[sphinx configuration]: https://www.sphinx-doc.org/en/master/usage/configuration.html
[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild
[sphinx-click]: https://sphinx-click.readthedocs.io/
[sphinx]: http://www.sphinx-doc.org/
[test fixture]: https://docs.pytest.org/en/latest/explanation/fixtures.html#about-fixtures
[testpypi]: https://test.pypi.org/
[toml]: https://github.com/toml-lang/toml
[tox]: https://tox.readthedocs.io/
[trailing-whitespace]: https://github.com/pre-commit/pre-commit-hooks#trailing-whitespace
[type annotations]: https://docs.python.org/3/library/typing.html
[typeguard]: https://github.com/agronholm/typeguard
[unix-style line endings]: https://en.wikipedia.org/wiki/Newline
[versions and constraints]: https://python-poetry.org/docs/dependency-specification/
[virtual environment]: https://docs.python.org/3/tutorial/venv.html
[virtualenv]: https://virtualenv.pypa.io/
[wheel]: https://www.python.org/dev/peps/pep-0427/
[xdoctest]: https://github.com/Erotemic/xdoctest
[yaml]: https://yaml.org/
