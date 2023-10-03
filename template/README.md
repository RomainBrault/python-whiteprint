{% include "jinja_template/license_header.md.j2" %}
<h1 align="center">
  <a href="https://{{project_slug}}.readthedocs.io/"><img src="https://raw.githubusercontent.com/{{github_user}}/{{project_slug}}/main/docs/images/logo.png" alt="python whiteprint"></a>
</h1>
<p align="center">
    <em>{{project_name}}, lorem ipsum et dolor si amet, consectetur adipiscing elit.</em>
</p>
<p align="center">
{% if spdx_license != "None" %}
  <a href="https://pypi.python.org/pypi/{{project_slug}}">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/{{project_slug}}.svg"/>
  </a>
{%- endif %}
{%- if ci == "github" %}
  <a href="https://github.com/{{github_user}}/{{project_slug}}/actions/workflows/tests.yml">
    <img alt="PyPI" src="https://github.com/{{github_user}}/{{project_slug}}/actions/workflows/tests.yml/badge.svg?branch=main"/>
  </a>
  <a href="https://codecov.io/gh/{{github_user}}/{{project_slug}}">
    <img alt="pypi" src="https://codecov.io/gh/{{github_user}}/{{project_slug}}/branch/main/graph/badge.svg?token=GSYS7VUB5R"/>
  </a>
{%- elif ci == "gitlab" %}
{%- else %}
{%- endif %}
  <a href="https://github.com/psf/black">
    <img alt="pypi" src="https://img.shields.io/badge/code%20style-black-000000.svg"/>
  </a>
  <a href="https://mypy-lang.org/">
    <img alt="pypi" src="https://www.mypy-lang.org/static/mypy_badge.svg"/>
  </a>
  <a href="https://pre-commit.com/">
    <img alt="pypi" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"/>
  </a>
{%- if spdx_license != "None" %}
  <a href="https://opensource.org/licenses/MIT">
    <img alt="pypi" src="https://img.shields.io/github/license/{{github_user}}/{{project_slug}}"/>
  </a>
{%- endif %}
  <a href="https://www.contributor-covenant.org/version/2/1/code_of_conduct/">
    <img alt="pypi" src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg"/>
  </a>
</p>

---
{% if documentation == "readthedocs" %}
**Documentation**: <a href="https://{{project_slug}}.readthedocs.io/en/latest/" target="_blank">https://{{project_slug}}.readthedocs.io/en/latest/</a>
{%- endif %}

**Source Code**: <a href="https://github.com/{{github_user}}/{{project_slug}}" target="_blank">https://github.com/{{github_user}}/{{project_slug}}</a>

---

# {{project_name}}

Welcome to {{project_name}}!

# Features

- Feature 1
- Feature 2
- ...

[cookiecutter-hypermodern-python]: https://cookiecutter-hypermodern-python.readthedocs.io/en/2022.6.3.post1/
[python-blueprint]: https://github.com/johnthagen/python-blueprint
