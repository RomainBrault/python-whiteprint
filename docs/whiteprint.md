<!--
SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>

SPDX-License-Identifier: MIT
-->

# Python Whiteprint User Guide

:::{warning}
This page is under construction
:::

This is the user guide for the [Python Whiteprint] a Python template based on
the [Hypermodern Python] article series. If you're in a hurry, check out the
[quickstart guide](quickstart) and the [tutorials](tutorials).

## About this project

**Python Whiteprint** is a general-purpose template for Python libraries and
applications, released under the [MIT license] and hosted on [GitHub][python whiteprint].

It follows the same goals as [Hypermodern Python Cookiecutter], but with
different tools. The main objective of this project template is to enable
current best practices through modern Python tooling. Our goals are to:

- focus on simplicity and minimalism,
- promote code quality through automation,
- provide reliable and repeatable processes,

all the way from local testing to publishing releases.

Projects are created from the template using [Copier], a project
scaffolding tool built on top of the [Jinja] template engine.

The project template is centered around the following tools:

- [Poetry] for packaging and dependency management
- [Nox] for automation of checks and other development tasks
- [GitHub Actions] for continuous integration and delivery

## Version policy

Python Whiteprint uses [Semantic Versioning].

(installation)=

## Installation

### System requirements

You need a recent Windows, Linux, Unix, or Mac system with [git] installed.

:::{note}
When working with this template on Windows, configure your text editor or IDE
to use only [UNIX-style line endings] (line feeds).

The project template contains a [.gitattributes] file which enables end-of-line
normalization for your entire working tree. Additionally, the [Prettier] code
formatter converts line endings to line feeds. Windows-style line endings
(`CRLF`) should therefore never make it into your Git repository.

Nonetheless, configuring your editor for line feeds is recommended to avoid
complaints from the [pre-commit] hook for Prettier.
:::

### Getting Python (Windows)

:::{warning}
Windows support is currently experimental and untested.
:::

If you're on Windows, download the recommended installer for the latest stable
release of Python from the official [Python website]. Before clicking **Install
now**, enable the option to add Python to your `PATH` environment variable.

Verify your installation by checking the output of the following commands in a
new terminal window:

```
python -VV
py -VV
```

Both of these commands should display the latest Python version.

For local testing with multiple Python versions, repeat these steps for the
latest bugfix releases of Python 3.7+, with the following changes:

- Do _not_ enable the option to add Python to the `PATH` environment variable.
- `py -VV` and `python -VV` should still display the version of the latest
  stable release.
- `py -X.Y -VV` (e.g. `py -3.11 -VV`) should display the exact version you just
  installed.

Note that binary installers are not provided for security releases.

### Getting Python (Mac, Linux, Unix)

#### Pyenv

If you're on a Mac, Linux, or Unix system, use [pyenv] for installing and
managing Python versions. Please refer to the documentation of this project for
detailed installation and usage instructions. (The following instructions
assume that your system already has [bash] and [curl] installed.)

Install [pyenv] like this:

```console
$ curl https://pyenv.run | bash
```

And follow the instructions.

Install the Python build dependencies for your platform, using one of the
commands listed in the [official instructions][pyenv wiki].

Install the latest point release of every supported Python version. For example
if the latest supported version is 3.11.1, run

```console
$ pyenv install 3.11.1
```

After creating your project (see [below](creating-a-project)), you can make
these Python versions accessible in the project directory, using the following
command:

```console
$ pyenv local 3.11.1
```

The first version listed is the one used when you type plain `python`. Every
version can be used by invoking `python<major.minor>`. For example, use
`python3.11` to invoke Python 3.11

#### Mamba

Another way to install and manage python versions in separated virtual
environments is [Mamba]. You can install it using the following command:

```console
$ curl micro.mamba.pm/install.sh | bash
```

Then you can create and activate your isolated Python environment:

```console
$ mamba create -n <my_project_environment_name> python=3.11
$ mamba activate <my_project_environment_name>
```

For more information see the [official instructions][mamba user guide]

### Requirements

:::{note}
We recommend to use [pipx] to install Python tools which are not specific
to a single project. Please refer to the official documentation for detailed
installation and usage instructions. If you decide to skip `pipx` installation,
use [pip install] with the `--user` option instead.

You can [install pipx] with [pip].

```console
$ python3 -m pip install --user -U pipx
```

The advantage of [pipx] being that the different tools are installed in
separated virtual environments, minimizing the risks of problems.
:::

You need four tools to use this template:

- [Python Whiteprint] to create projects from the template,
- [Poetry] to manage packaging and dependencies
- [Nox] to automate checks and other tasks
- [nox-poetry] for using Poetry in Nox sessions
- [rich] for colorful outputs in [Nox]

Install [Python Whiteprint] using pipx:

```console
$ pipx install python-whiteprint
```

Install [Poetry] by downloading and running [install-poetry.py]:

```console
$ pipx install poetry
```

Install [Nox], [nox-poetry] and [rich] using pipx:

```console
$ pipx install nox
$ pipx inject nox nox-poetry rich
```

Remember to upgrade these tools regularly:

```console
$ pipx upgrade cookiecutter
$ pipx upgrade --include-injected nox
$ poetry self update
```

## Project creation

(creating-a-project)=

### Creating a project

After installation, create a project from this template by running

```console
$ whiteprint init <project_name>
```

[Copier] downloads the template, and asks you a series of questions about
project variables, for example, how you wish your project to be named. When you
have answered these questions, your project is generated in the current
directory, using a subdirectory with the same name as your project.

:::{note}
The initial project version should be the latest release on [PyPI], or `0.0.0`
for an unreleased package. See [The Release workflow](the-release-workflow) for
details.
:::

Your choices are recorded in the file `.copier-answers.yml` in the generated
project.

In the remainder of this guide, `<project>` and `<package>` are used to refer
to the project and package names, respectively. By default, their only
difference is that the project name uses hyphens (_kebab case_), whereas the
package name uses underscores (_snake case_).

### Uploading to GitHub

This project template is designed for use with [GitHub]. To create your package
on GitHub create a [GitHub token] and run the following command:

```console
$ whiteprint init <project_name> --github-token <github_token>
```

## How to use your Python Project once generated

Check out the [Project User Guide](./guide) to see how to use your generated
project!

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
