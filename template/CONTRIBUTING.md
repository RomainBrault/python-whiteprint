{% include "jinja_template/license_header.md.j2" %}
# 🛠️ Contributor Guide

Thank you for your interest in improving this project.
{%- if license != "None" %}
This project is open-source under the [{{license}}
license](https://opensource.org/licenses/{{license}}) and welcomes
contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:
{% else %}
This project welcomes contributions.
{% endif -%}
{% if documentation == "readthedocs" %}
- [Documentation](https://{{project_slug}}.readthedocs.io/en/latest/)
{%- endif %}
{%- if ci == "github" %}
- [Source Code](https://github.com/{{github_user}}/{{project_slug}}.git)
- [Issue Tracker](https://github.com/{{github_user}}/{{project_slug}}/issues)
{% elif ci == "gitlab" %}
{% else %}
{% endif -%}
{% if ci == "no_ci" -%}
## How to report a bug

Report bugs on the [Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker].
{% endif %}
## How to set up your development environment

You need Python {{target_python_version}}+ and the following tools:

- [Poetry]
- [Nox] with [nox-poetry], [rich] and [beartype] additional dependencies

Once your environment is set-up, install the package with development
requirements:

```console
$ poetry install
```

You can now run an interactive Python session,
or the command-line interface:

```console
$ poetry run python
$ poetry run {{package_name}}
```

To avoid prefixing all your commands by `poetry run` you can source a poetry
shell and then run an interactive Python session or the command-line interface:

```console
$ poetry shell
$ python
$ {{package_name}}
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
$ nox --session=tests
```

Unit tests are located in the _tests_ directory,
and are written using the [pytest] testing framework.

[pytest]: https://pytest.readthedocs.io/
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/
{% if ci != "no_ci" %}
## How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you
can install [pre-commit] as a Git hook by running the following command:

```console
$ nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.
{% if ci == "github" %}
[pull request]: https://github.com/{{github_user}}/{{project_slug}}/pulls
{% elif ci == "gitlab" %}
{% else %}
{% endif -%}
{% endif %}
<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md
[pre-commit]: https://pre-commit.com/
