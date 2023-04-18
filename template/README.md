{% include "jinja_template/license_header.md.j2" %}
# {{project_name}}
{% if spdx_license != "None" %}
[![PyPI Version](https://img.shields.io/pypi/v/{{project_slug}}.svg)](https://pypi.python.org/pypi/{{project_slug}})
{%- endif %}
{%- if documentation == "readthedocs" %}
[![Documentation](https://readthedocs.org/projects/{{project_slug}}/badge/?version=latest)](https://{{project_slug}}.readthedocs.io/en/latest)
{%- endif %}
{%- if ci == "github" %}
[![Tests](https://github.com/{{github_user}}/{{project_slug}}/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/{{github_user}}/{{project_slug}}/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/{{github_user}}/{{project_slug}}/branch/main/graph/badge.svg?token=GSYS7VUB5R)](https://codecov.io/gh/{{github_user}}/{{project_slug}})
{%- elif ci == "gitlab" %}
{%- else %}
{%- endif %}
[![Code style: black][black-badge]](https://github.com/psf/black)
[![Type checked with mypy][mypy-badge]](https://mypy-lang.org/)
[![pre-commit enabled][pre-commit badge]](https://pre-commit.com/)
{%- if spdx_license != "None" %}
[![License][license badge]](https://opensource.org/licenses/{{spdx_license}})
{%- endif %}
[![Contributor Covenant][contributor covenant badge]](https://www.contributor-covenant.org/version/2/1/code_of_conduct/)

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[mypy-badge]: https://www.mypy-lang.org/static/mypy_badge.svg
[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
{%- if spdx_license != "None" %}
[license badge]: https://img.shields.io/github/license/{{github_user}}/{{project_slug}}
{%- endif %}
[contributor covenant badge]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg

Welcome to {{project_name}}!

## Features

- Feature 1
- Feature 2
- ...

[cookiecutter-hypermodern-python]: https://cookiecutter-hypermodern-python.readthedocs.io/en/2022.6.3.post1/
[python-blueprint]: https://github.com/johnthagen/python-blueprint
