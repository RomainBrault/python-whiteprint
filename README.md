<!--
SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>

SPDX-License-Identifier: MIT
-->

<h1 align="center">
  <a href="https://python-whiteprint.readthedocs.io/"><img src="https://raw.githubusercontent.com/RomainBrault/python-whiteprint/main/docs/images/logo.png" alt="python whiteprint"></a>
</h1>
<p align="center">
  <a href="https://pypi.python.org/pypi/python-whiteprint">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/python-whiteprint.svg"/>
  </a>
  <a href="https://github.com/RomainBrault/python-whiteprint/actions/workflows/tests.yml">
    <img alt="PyPI" src="https://github.com/RomainBrault/python-whiteprint/actions/workflows/tests.yml/badge.svg?branch=main"/>
  </a>
  <a href="https://codecov.io/gh/RomainBrault/python-whiteprint">
    <img alt="pypi" src="https://codecov.io/gh/RomainBrault/python-whiteprint/branch/main/graph/badge.svg?token=GSYS7VUB5R"/>
  </a>
  <a href="https://github.com/psf/black">
    <img alt="pypi" src="https://img.shields.io/badge/code%20style-black-000000.svg"/>
  </a>
  <a href="https://mypy-lang.org/">
    <img alt="pypi" src="https://www.mypy-lang.org/static/mypy_badge.svg"/>
  </a>
  <a href="https://pre-commit.com/">
    <img alt="pypi" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img alt="pypi" src="https://img.shields.io/github/license/RomainBrault/python-whiteprint"/>
  </a>
  <a href="https://www.contributor-covenant.org/version/2/1/code_of_conduct/">
    <img alt="pypi" src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg"/>
  </a>
</p>
<p align="center">
    <em>Python Whiteprint, generate easily Python projects with (opinionated) best practices.</em>
</p>

---

**Documentation**: <a href="https://python-whiteprint.readthedocs.io/en/latest/" target="_blank">https://python-whiteprint.readthedocs.io/en/latest/</a>

**Source Code**: <a href="https://github.com/RomainBrault/python-whiteprint" target="_blank">https://github.com/RomainBrault/python-whiteprint</a>

---

# Yet another Python Project scaffold/cookiecutter/generator?

<p align="center"><em>
Yes.
</em></p>

This project build upon the excellents [cookiecutter-hypermodern-python] by
[@cjolowicz](https://github.com/cjolowicz) as well as [python-blueprint] by
[@johnthagen](https://github.com/johnthagen).

You might want to check these project as they might be more suited to your
needs.

# Differences compared to [cookiecutter-hypermodern-python]

- [x] Use [copier](https://copier.readthedocs.io/en/latest/) instead of the
      unmainted cookiecutter,
- [x] tweaks in the generated project (non exhaustively: CLI with Typer
      instead of Click, dynamic type checking with beartype, [auto-API
      documentation](https://sphinx-autoapi.readthedocs.io/en/latest/)),
- [x] manage licenses with [Reuse](https://reuse.software/),
- [x] more Github Actions and Community Standards and Community Standards,
- [x] Ruff instead of Flake8 to fix a maximum of code smells,
- [x] strict linting with pylint,
- [x] OCI Container images,
- [ ] basic GitLab support,
- [ ] Latex template with python integration.

[cookiecutter-hypermodern-python]: https://cookiecutter-hypermodern-python.readthedocs.io/en/2022.6.3.post1/
[python-blueprint]: https://github.com/johnthagen/python-blueprint
