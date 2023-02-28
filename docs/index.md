# User Guide

!!! info

    For more information on how this was built and deployed, as well as other
    Python best practices, see
    [`python-whiteprint`](https://github.com/RomainBrault/python-whiteprint).

!!! info

    This user guide is purely an illustrative example that shows off several
    features of [Material for
    MkDocs](https://squidfunk.github.io/mkdocs-material/) and included Markdown
    extensions[^1].

[^1]: See `python-whiteprint`'s `mkdocs.yml` for how to enable these features.

## Installation

To install from the sources, after obtaining a copy of them on
[GitHub](https://github.com/RomainBrault/python-whiteprint).

```bash
pip install .
```

For development purposes, you can use
[Poetry](https://python-poetry.org/docs/#installation) to install the project
from the sources. More information is available in the
[CONTRIBUTING](CONTRIBUTING.md) guide.

## Quick Start

This project is an example of a simple
[Typer](https://github.com/tiangolo/typer) [command-line
interface](https://en.wikipedia.org/wiki/Command-line_interface) (CLI).

```python
from python_whiterprint import hello_world

assert hello_world.hello_world() == "Hello, World!"
```

1. This assertion will be `True`

!!! tip

    Within PyCharm, use ++tab++ to auto-complete suggested imports while
    typing.
