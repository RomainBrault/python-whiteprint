<!--
SPDX-FileCopyrightText: 2023 Romain Brault <mail@romainbrault.com>

SPDX-License-Identifier: MIT
-->

# Python Whiteprint

[![PyPI Version](https://img.shields.io/pypi/v/python-whiteprint.svg)](https://pypi.python.org/pypi/python-whiteprint)
[![Documentation](https://readthedocs.org/projects/python-whiteprint/badge/?version=latest)](https://python-whiteprint.readthedocs.io/en/latest/?badge=latest)
[![Tests](https://github.com/RomainBrault/python-whiteprint/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/RomainBrault/python-whiteprint/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/RomainBrault/python-whiteprint/branch/main/graph/badge.svg?token=GSYS7VUB5R)](https://codecov.io/gh/RomainBrault/python-whiteprint)
[![Code style: black][black-badge]](https://github.com/psf/black)
[![Type checked with mypy][mypy-badge]](https://mypy-lang.org/)
[![pre-commit enabled][pre-commit badge]](https://pre-commit.com/)
[![License][license badge]](https://opensource.org/licenses/MIT)
[![Contributor Covenant][contributor covenant badge]](https://github.com/RomainBrault/python-whiteprint/blob/main/CODE_OF_CONDUCT.md)

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[mypy-badge]: https://www.mypy-lang.org/static/mypy_badge.svg
[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[license badge]: https://img.shields.io/github/license/cjolowicz/cookiecutter-hypermodern-python
[contributor covenant badge]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg

Cookiecutter to create a Python package using modern Python testing,
linting, and type checking tooling.

## Yet another Python Project cookiecutter?

Yes.

This project build upon the excellents [cookiecutter-hypermodern-python] by
[@cjolowicz](https://github.com/cjolowicz) as well as [python-blueprint] by
[@johnthagen](https://github.com/johnthagen).

You might want to check these project as they might be more suited to your
needs.

## Differences compared to [cookiecutter-hypermodern-python]

- [ ] Tweaks in the generated project (non exhaustively: CLI with Typer
      instead of Click, dynamic type checking with beartype, [auto-API
      documentation](https://sphinx-autoapi.readthedocs.io/en/latest/)),
- [ ] manage licenses with [Reuse](https://reuse.software/),
- [ ] more Github Actions and Community Standards and Community Standards,
- [ ] Ruff instead of Flake8 to fix a maximum of code smells,
- [ ] strict linting with pylint,
- [ ] OCI Container images,
- [ ] basic GitLab support,
- [ ] Latex template with python integration.

[cookiecutter-hypermodern-python]: https://cookiecutter-hypermodern-python.readthedocs.io/en/2022.6.3.post1/
[python-blueprint]: https://github.com/johnthagen/python-blueprint
