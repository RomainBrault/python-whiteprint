"""Automates testing in banditmultiple Python environments."""
import os
import pathlib
import shlex
import shutil
import tempfile
import textwrap

import nox_poetry
import packaging
from beartype import beartype
from beartype.typing import Dict, List
from nox import options
from rich import console


CONSOLE = console.Console()


PYTHON_VERSIONS = sorted(
    ["3.8", "3.9", "3.10", "3.11"],
    key=packaging.version.Version,
)
WORKING_PYTHON_VERSION = PYTHON_VERSIONS[-1]

options.sessions = [
    "pip-audit",
    "pre-commit",
    "test",
    "docs-build",
]


@beartype
def _not_hook(hook: pathlib.Path) -> bool:
    return hook.name.endswith(".sample") or not hook.is_file()


@beartype
def _patch_hook(
    hook: pathlib.Path,
    *,
    headers: Dict[str, str],
    lines: List[str],
) -> None:
    for executable, header in headers.items():
        if executable in lines[0].lower():
            lines.insert(1, textwrap.dedent(header))
            hook.write_text("\n".join(lines))
            break


@beartype
def _bindir_in_hook(bindirs: List[str], *, text: str) -> bool:
    return any(
        (
            (
                pathlib.Path("A") == pathlib.Path("a")
                and bindir.lower() in text.lower()
            )
            or bindir in text
        )
        for bindir in bindirs
    )


@beartype
def _patch_hooks(
    hookdir: pathlib.Path,
    *,
    bindirs: List[str],
    headers: Dict[str, str],
) -> None:
    for hook in hookdir.iterdir():
        if _not_hook(hook) or not hook.read_bytes().startswith(b"#!"):
            continue

        text = hook.read_text()

        if not _bindir_in_hook(bindirs, text=text):
            continue

        lines = text.splitlines()
        _patch_hook(hook, headers=headers, lines=lines)


@beartype
def activate_virtualenv_in_precommit_hooks(
    session: nox_poetry.Session,
) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.

    Note:
        Adapted from Claudio Jolowicz <mail@claudiojolowicz.com>:
        https://github.com/cjolowicz/cookiecutter-hypermodern-python
    """
    # Only patch hooks containing a reference to this session's bindir. Support
    # quoting rules for Python and bash, but strip the outermost quotes so we
    # can detect paths within the bindir, like <bindir>/python.
    bindirs = [
        bindir[1:-1] if bindir[0] in "'\"" else bindir
        for bindir in (repr(session.bin), shlex.quote(session.bin))
    ]

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    headers = {
        # pre-commit < 2.16.0
        "python": f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """,
        # pre-commit >= 2.16.0
        "bash": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
        # pre-commit >= 2.17.0 on Windows forces sh shebang
        "/bin/sh": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
    }

    hookdir = pathlib.Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    _patch_hooks(hookdir, bindirs=bindirs, headers=headers)


@beartype
def install_poetry_groups(
    session: nox_poetry.Session,
    *groups: str,
) -> None:
    """Install dependencies from poetry groups.

    Args:
        session: The Session object.
        *groups: groups to install.
        only: only install specific dependency group.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            *(f"--with={group}" for group in groups),
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("-r", requirements.name)


@nox_poetry.session(name="pre-commit", python=WORKING_PYTHON_VERSION)
@beartype
def pre_commit(session: nox_poetry.Session) -> None:
    """Lint and format using pre-commit.

    Args:
        session: The Session object.
    """
    args = session.posargs or [
        "run",
        "--all-files",
        "--hook-stage=manual",
        "--show-diff-on-failure",
    ]
    session.install(".")
    install_poetry_groups(
        session,
        "nox",
        "test",
        "lint",
        "type_check",
        "fmt",
        "pre-commit",
        "complexity",
        "docs",
    )
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def coverage(session: nox_poetry.Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report", "--skip-covered"]

    install_poetry_groups(session, "coverage")

    if not session.posargs and any(pathlib.Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)
    session.run("coverage", "xml")
    session.run("coverage", "lcov")
    session.run("coverage", "html")
    session.run("coverage", "erase")


@nox_poetry.session(python=PYTHON_VERSIONS)
@beartype
def test(session: nox_poetry.Session) -> None:
    """Run the tests suite and append coverage to the existing one.

    Args:
        session: The Session object.
    """
    session.install(".")
    install_poetry_groups(session, "test", "coverage")
    try:
        session.run(
            "pytest",
            "--cov-report=term-missing:skip-covered",
            "tests",
            "src/python_whiteprint",
            *session.posargs,
            env={
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONOPTIMIZE": "0",
            },
        )
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def fmt(session: nox_poetry.Session) -> None:
    """Format the code.

    Args:
        session: The Session object.
    """
    install_poetry_groups(session, "fmt")
    session.run("black", ".")
    session.run("isort", ".")
    session.run("ruff", "--fix-only", ".")


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def lint(session: nox_poetry.Session) -> None:
    """Lint the code with PyLint.

    Args:
        session: The Session object.
    """
    session.install(".")
    install_poetry_groups(
        session,
        "nox",
        "test",
        "lint",
        "type_check",
        "fmt",
        "pre-commit",
        "docs",
    )
    session.run(
        "pylint",
        "--output-format=colorized",
        "src",
        "tests",
        "docs",
    )


@nox_poetry.session(name="type-check", python=WORKING_PYTHON_VERSION)
@beartype
def type_check(session: nox_poetry.Session) -> None:
    """Type check the code.

    Args:
        session: The Session object.
    """
    session.install(".")
    install_poetry_groups(
        session,
        "nox",
        "test",
        "lint",
        "type_check",
        "fmt",
        "pre-commit",
        "docs",
        "type_check",
    )
    session.run("mypy", ".")


# Environment variable needed for mkdocstrings-python to locate source files.
DOC_ENV = {"PYTHONPATH": "src"}


@nox_poetry.session(name="pip-audit", python=PYTHON_VERSIONS)
@beartype
def pip_audit(session: nox_poetry.Session) -> None:
    """Scan dependencies for insecure packages.

    Argsf:
        session: The Session object.
    """
    session.run_always(
        "poetry",
        "install",
        "--no-root",
        "--no-dev",
        external=True,
        silent=True,
    )
    session.install("pip-audit")
    session.run("pip-audit", "--strict")


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def bandit(session: nox_poetry.Session) -> None:
    """Lint source code for security issues.

    Args:
        session: The Session object.
    """
    args = session.posargs or [
        "--recursive",
        "--configfile",
        "pyproject.toml",
        "src/",
        "docs/*.py",
        "tests/",
    ]
    session.install("bandit")
    session.run("bandit", *args)


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def radon(session: nox_poetry.Session) -> None:
    """Measure the Maintainability Index of the code.

    Args:
        session: The Session object.
    """
    args = session.posargs or [
        "mi",
        "src/",
        "docs/",
        "tests/",
    ]
    session.install("radon")
    session.run("radon", *args)


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def xenon(session: nox_poetry.Session) -> None:
    """Check the Maintainability Index of the code.

    Args:
        session: The Session object.
    """
    args = session.posargs or [
        "--max-average",
        "A",
        "--max-modules",
        "A",
        "--max-absolute",
        "A",
        "--ignore",
        "noxfile.py",
        "src/",
        "tests/",
    ]
    session.install("xenon")
    session.run("xenon", *args)


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def licenses(session: nox_poetry.Session) -> None:
    """List the licenses.

    Args:
        session: The Session object.
    """
    session.run_always(
        "poetry",
        "install",
        "--no-root",
        "--no-dev",
        external=True,
        silent=True,
    )
    session.install("pip-licenses")
    licenses_table = session.run(
        "pip-licenses",
        "--from=mixed",
        "--with-urls",
        *session.posargs,
        silent=True,
    )
    CONSOLE.print(licenses_table)


@beartype
def _export_licenses(session: nox_poetry.Session) -> None:
    session.posargs = [
        "--from=mixed",
        "--with-urls",
        "--format=markdown",
        "--output-file=DEPENDENCIES.md",
    ]
    licenses(session)


@nox_poetry.session(name="docs-build", python=WORKING_PYTHON_VERSION)
@beartype
def docs_build(session: nox_poetry.Session) -> None:
    """Build the documentation.

    Args:
        session: The Session object.
    """
    args = session.posargs or ["-W", "--keep-going", "docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    _export_licenses(session)

    session.install(".")
    install_poetry_groups(session, "docs")

    build_dir = pathlib.Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@nox_poetry.session(python=WORKING_PYTHON_VERSION)
@beartype
def docs(session: nox_poetry.Session) -> None:
    """Build and serve the documentation with live reloading on file changes.

    Args:
        session: The Session object.
    """
    args = session.posargs or [
        "-W",
        "--open-browser",
        "docs",
        "docs/_build",
    ]

    _export_licenses(session)

    session.install(".")
    install_poetry_groups(session, "docs")

    build_dir = pathlib.Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)


@nox_poetry.session(name="docs-check-links", python=WORKING_PYTHON_VERSION)
@beartype
def docs_check_links(session: nox_poetry.Session) -> None:
    """Build the documentation."""
    args = session.posargs or [
        "-b",
        "linkcheck",
        "-W",
        "--keep-going",
        "docs",
        "docs/_build",
    ]

    builddir = pathlib.Path("docs", "_build")
    if builddir.exists():
        shutil.rmtree(builddir)

    session.install(".")
    install_poetry_groups(session, "docs")

    session.run("sphinx-build", *args)
