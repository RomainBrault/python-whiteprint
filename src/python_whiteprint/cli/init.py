# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Initialize a new Python project."""

import enum
import importlib
import logging
import os
import pathlib
import shutil

import platformdirs
from beartype import beartype
from beartype.typing import Any, Dict, List, Optional, Union
from click import core, exceptions
from typer import params
from typing_extensions import TypeGuard

from python_whiteprint.loc import _


YAML_EXT = [".yaml", ".yml"]
COPIER_ANSWER_FILE = ".copier-answers.yml"
LABEL_FILE = ".github/labels.yml"


@beartype
class UnsupportedTypeInMapping(exceptions.UsageError):
    """The given type is not supported."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__("The mapping contains unsupported type")


@beartype
class NotAValidYAML(exceptions.UsageError):
    """The YAML file is invalid."""

    def __init__(self, path: pathlib.Path, error: str) -> None:
        """Initialize the exception.

        Args:
            path: path to the invalid YAML file.
            error: the parser error message.
        """
        super().__init__(f"{path} is not a valid YAML file, {error}.")


class DefaultVenvBackend(str, enum.Enum):
    """Nox's default virtual environments backend."""

    NONE = "NONE"
    VIRTUALENV = "VIRTUALENV"
    CONDA = "CONDA"
    MAMBA = "MAMBA"
    VENV = "VENV"


@beartype
def read_yaml(data: pathlib.Path) -> Dict[str, Union[str, int]]:
    """Read a yaml file.

    Use PyYAML `safe_load`.

    Args:
        data: path to the YAML file. The file must exists.

    Returns:
        The content of the YAML file.
    """
    if not data.is_file():
        return {}

    yaml = importlib.import_module("yaml")
    with data.open("r") as data_file:
        try:
            copier_data = yaml.safe_load(data_file)
        except yaml.parser.ParserError as parser_error:
            raise NotAValidYAML(data, str(parser_error)) from parser_error

        if _check_dict(copier_data):
            return copier_data

    raise UnsupportedTypeInMapping


@beartype
def _copy_license_to_project_root(destination: pathlib.Path) -> None:
    """Add the license to the COPYING file.

    Forward the license or copyright header from the LICENSE directory to the
    COPYING file.

    Args:
        destination: path to the python project.
    """
    license_name = (
        (destination / "COPYING").read_text(encoding="utf-8").strip()
    )
    license_path = destination / "LICENSES" / f"{license_name}.txt"
    if license_path.is_file():
        shutil.copy(
            license_path,
            destination / "COPYING",
        )


@beartype
def _format_code(
    destination: pathlib.Path,
    *,
    default_venv_backend: DefaultVenvBackend,
    python: Optional[str],
) -> None:
    """Reformat the source code with pre-commit if needed.

    Args:
        destination: path to the python project.
        default_venv_backend: default virtual environment backend for Nox.
        python: force using the given python interpreter for the post
            processing.
    """
    nox = importlib.import_module(
        "python_whiteprint.nox",
        __package__,
    )
    try:
        nox.run(
            destination=destination,
            args=[
                "--default-venv-backend",
                default_venv_backend.value.lower(),
                *(("--force-python", python) if python else ()),
                "--session",
                "pre-commit",
            ],
        )
    except nox.NoxError as nox_error:
        logger = logging.getLogger(__name__)
        logger.debug(
            "Code has been reformated (Nox exit code: %s).",
            nox_error.exit_code,
        )


@beartype
def _download_licenses(
    destination: pathlib.Path,
    *,
    default_venv_backend: DefaultVenvBackend,
    python: Optional[str],
) -> None:
    """Download the needed licenses.

    Args:
        destination: path to the python project.
        default_venv_backend: default virtual environment backend for Nox.
        python: force using the given python interpreter for the post
            processing.
    """
    nox = importlib.import_module(
        "python_whiteprint.nox",
        __package__,
    )
    nox.run(
        destination=destination,
        args=[
            "--default-venv-backend",
            default_venv_backend.value.lower(),
            *(("--force-python", python) if python else ()),
            "--session",
            "reuse",
            "--",
            "download",
            "--all",
        ],
    )

    _copy_license_to_project_root(destination)


@beartype
def _post_processing(
    destination: pathlib.Path,
    *,
    default_venv_backend: DefaultVenvBackend,
    skip_tests: bool,
    python: Optional[str],
    github_token: Optional[str],
    https_origin: bool,
) -> None:
    """Apply post processing steps after rendering the template wit Copier.

    Args:
        destination: path to the python project.
        default_venv_backend: default virtual environment backend for Nox.
        skip_tests: skip the Nox tests step.
        python: force using the given python interpreter for the post
            processing.
        github_token: Github Token to push the newly created repository to
            Github. The token must have writing permissions.
        https_origin: force the origin to be an HTTPS URL.
    """
    git = importlib.import_module(
        "python_whiteprint.git",
        __package__,
    )
    nox = importlib.import_module(
        "python_whiteprint.nox",
        __package__,
    )
    poetry = importlib.import_module(
        "python_whiteprint.poetry",
        __package__,
    )

    # Create poetry.lock
    poetry.lock(destination)
    repository = git.init_and_commit(destination)

    # Download the required licenses.
    _download_licenses(
        destination, default_venv_backend=default_venv_backend, python=python
    )
    git.add_and_commit(repository, message="chore: 📃 download license(s).")

    # Generate the dependencies table.
    nox.run(
        destination=destination,
        args=[
            "--default-venv-backend",
            default_venv_backend.value.lower(),
            *(("--force-python", python) if python else ()),
            "--session",
            "licenses",
            "--",
            "--from=mixed",
            "--with-urls",
            "--format=markdown",
            "--output-file=DEPENDENCIES.md",
        ],
    )
    git.add_and_commit(repository, message="docs: 📚 add depencencies.")

    # Fixes with pre-commit.
    _format_code(
        destination, default_venv_backend=default_venv_backend, python=python
    )
    git.add_and_commit(repository, message="chore: 🔨 format code.")

    # Check that nox passes.
    if not skip_tests:
        nox.run(
            destination=destination,
            args=[
                "--default-venv-backend",
                default_venv_backend.value.lower(),
                *(("--force-python", python) if python else ()),
            ],
        )

    if github_token:
        copier_answers = read_yaml(destination / COPIER_ANSWER_FILE)
        git.setup_github_repository(
            repository,
            project_slug=copier_answers["project_slug"],
            github_token=github_token,
            github_login=copier_answers["github_user"],
            labels=destination / LABEL_FILE,
        )
        git.protect_repository(
            repository,
            project_slug=copier_answers["project_slug"],
            github_token=github_token,
            github_login=copier_answers["github_user"],
            https_origin=https_origin,
        )


@beartype
def _autocomplete_suffix(incomplete: pathlib.Path) -> List[str]:
    """Autocomplete by listing files with a YAML extension.

    Args:
        incomplete: the incomplete argument to complete. Must be a path to a
            file with a suffix.

    Returns:
        A list of completions.
    """
    if all(incomplete.suffix not in ext for ext in YAML_EXT):
        return []

    return [
        candidate.name
        for candidate in incomplete.parent.glob(f"{incomplete.name}*")
    ]


@beartype
def autocomplete_yaml_file(
    _ctx: Optional[core.Context],
    _param: Optional[core.Parameter],
    incomplete: str,
) -> List[str]:
    """Autocomplete by listing files with a YAML extension.

    Args:
        _ctx: unused
        _param: unused
        incomplete: the incomplete argument to complete.

    Returns:
        A list of completions.
    """
    path = pathlib.Path(incomplete)
    if path.suffix:
        return _autocomplete_suffix(path)

    if path.is_dir():
        name = ""
    else:
        name = path.stem
        path = path.parent

    proposal: List[str] = []
    for ext in YAML_EXT:
        candidates = path.glob(f"{name}*{ext}")
        proposal.extend(candidate.name for candidate in candidates)

    return proposal


_argument_destination = params.Argument(
    ".",
    exists=False,
    file_okay=False,
    dir_okay=True,
    writable=True,
    readable=False,
    resolve_path=True,
    metavar="DIRECTORY",
    help=_("Destination path where to create the Python project."),
)
"""see `python_whiteprint.cli.init.init` argument `destination`."""
_option_src_path = params.Option(
    os.environ.get(
        "WHITEPRINT_REPOSITORY",
        "gh:RomainBrault/python-whiteprint.git",
    ),
    "--whiteprint-source",
    "-w",
    envvar="WHITEPRINT_REPOSITORY",
    help=_(
        "The location of the Python Whiteprint Git repository (string that"
        " can be resolved to a template path, be it local or remote)."
    ),
)
"""see `python_whiteprint.cli.init.init` option `src_path`."""
_option_vcs_ref = params.Option(
    os.environ.get("WHITEPRINT_VCS_REF"),
    "--vcs-ref",
    "-v",
    envvar="WHITEPRINT_VCS_REF",
    help=_(
        "Specify the VCS tag/commit to use in the Python Whiteprint Git"
        " repository."
    ),
)
"""see `python_whiteprint.cli.init.init` option `vcs_ref`."""
_option_exclude = params.Option(
    (),
    "--exclude",
    "-x",
    help=_(
        "User-chosen additional file exclusion patterns. Can be repeated"
        " to ignore multiple files."
    ),
)
"""see `python_whiteprint.cli.init.init` option `exclude`."""
_option_use_prereleases = params.Option(
    False,
    "--use-prereleases",
    "-P",
    help=_(
        "Consider prereleases when detecting the latest one. Useless if"
        " specifying a --vcs-ref."
    ),
)
"""see `python_whiteprint.cli.init.init` option `use_prereleases`."""
_option_skip_if_exists = params.Option(
    (),
    "--skip-if-exsists",
    "-s",
    help=_(
        "User-chosen additional file skip patterns. Can be repeated to"
        " ignore multiple files."
    ),
)
"""see `python_whiteprint.cli.init.init` option `skip_if_exists`."""
_option_cleanup_on_error = params.Option(
    False,
    "--no-cleanup-on-error",
    "-C",
    help=_("Do NOT delete the destination DIRECTORY if there is an error."),
)
"""see `python_whiteprint.cli.init.init` option `cleanup_on_error`."""
_option_defaults = params.Option(
    False,
    "--defaults",
    "-D",
    help=_(
        "Use default answers to questions, which might be null if not"
        " specified."
    ),
)
"""see `python_whiteprint.cli.init.init` option `defaults`."""
_option_overwrite = params.Option(
    False,
    "--overwrite",
    "-O",
    help=_("When set, overwrite files that already exist, without asking."),
)
"""see `python_whiteprint.cli.init.init` option `overwrite`."""
_option_pretend = params.Option(
    False,
    "--pretend",
    "-P",
    help=_("When set, produce no real rendering."),
)
"""see `python_whiteprint.cli.init.init` option `prepend`."""
_option_quiet = params.Option(
    False,
    "--quiet",
    "-Q",
    help=_("When set, disable all output."),
)
"""see `python_whiteprint.cli.init.init` option `quiet`."""
_option_default_venv_backend = params.Option(
    os.environ.get("WHITEPRINT_DEFAULT_VENV_BACKEND", "VIRTUALENV"),
    "--default-venv-backend",
    "-b",
    case_sensitive=False,
    envvar="WHITEPRINT_DEFAULT_VENV_BACKEND",
    help=_("Default virtual environment backend for Nox."),
)
"""see `python_whiteprint.cli.init.init` option `default_venv_backend`."""
_option_skip_tests = params.Option(
    os.environ.get("WHITEPRINT_SKIP_TESTS", False),
    "--skip-tests",
    "-S",
    envvar="WHITEPRINT_SKIP_TESTS",
    help=_("Skip tests after initializing the repository."),
)
"""see `python_whiteprint.cli.init.init` option `skip_tests`."""
_option_user_defaults = params.Option(
    os.environ.get("WHITEPRINT_USER_DEFAULTS"),
    "--user-defaults",
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    shell_complete=autocomplete_yaml_file,
    envvar="WHITEPRINT_USER_DEFAULTS",
    help=_("User defaults choices."),
)
"""see `python_whiteprint.cli.init.init` option `user_defaults`."""
_option_no_data = params.Option(
    False,
    "--no-data",
    "-n",
    help=_("Force not using --data."),
)
"""see `python_whiteprint.cli.init.init` option `no_data`."""
_option_data = params.Option(
    os.environ.get(
        "WHITEPRINT_DATA",
        (
            pathlib.Path(platformdirs.user_config_dir("whiteprint"))
            / "config.yml"
        ),
    ),
    "--data",
    exists=False,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    shell_complete=autocomplete_yaml_file,
    envvar="WHITEPRINT_DATA",
    help=_("User data."),
)
"""see `python_whiteprint.cli.init.init` option `user_data`."""
_option_python = params.Option(
    os.environ.get("WHITEPRINT_PYTHON"),
    "--python",
    "-p",
    envvar="WHITEPRINT_PYTHON",
    help=_(
        "force using the given python interpreter for the post processing."
    ),
)
"""see `python_whiteprint.cli.init.init` option `python`."""
_option_github_token = params.Option(
    os.environ.get("WHITEPRINT_GITHUB_TOKEN"),
    "--github-token",
    help=_(
        "Github Token to push the newly created repository to Github. The"
        " token must have writing permissions."
    ),
    envvar="WHITEPRINT_GITHUB_TOKEN",
)
"""see `python_whiteprint.cli.init.init` option `github_token`."""
_option_https_origin = params.Option(
    os.environ.get("WHITEPRINT_HTTPS_ORIGIN", False),
    "--https-origin",
    "-H",
    envvar="WHITEPRINT_HTTPS_ORIGIN",
    help=_("Force the origin to be an https URL."),
)
"""see `python_whiteprint.cli.init.init` option `https_origin`."""


@beartype
def _check_dict(data: Dict[str, Any]) -> TypeGuard[Dict[str, Union[str, int]]]:
    """Check if the values type of a given dictionary are strings or integers.

    Args:
        data: the dictionary to check:

    Returns:
        a boolean (type guard) indicating whether the values are all strings or
        integers.
    """
    return all(isinstance(v, (str, int)) for v in data.values())


@beartype
def init(  # pylint: disable=too-many-locals
    *,
    destination: pathlib.Path = _argument_destination,
    src_path: str = _option_src_path,
    vcs_ref: Optional[str] = _option_vcs_ref,
    exclude: List[str] = _option_exclude,
    use_prereleases: bool = _option_use_prereleases,
    skip_if_exists: List[str] = _option_skip_if_exists,
    cleanup_on_error: bool = _option_cleanup_on_error,
    defaults: bool = _option_defaults,
    overwrite: bool = _option_overwrite,
    pretend: bool = _option_pretend,
    quiet: bool = _option_quiet,
    default_venv_backend: DefaultVenvBackend = _option_default_venv_backend,
    skip_tests: bool = _option_skip_tests,
    data: pathlib.Path = _option_data,
    no_data: bool = _option_no_data,
    user_defaults: Optional[pathlib.Path] = _option_user_defaults,
    python: Optional[str] = _option_python,
    github_token: Optional[str] = _option_github_token,
    https_origin: bool = _option_https_origin,
) -> None:
    """Initalize a new Python project.

    This command mostly forwards copier's CLI. For more details see
    https://copier.readthedocs.io/en/stable/reference/cli/#copier.cli.CopierApp.

    Args:
        destination: destination path where to create the Python project.
        src_path: the location of the Python Whiteprint Git repository (string
            that can be resolved to a template path, be it local or remote).
        vcs_ref: specify the VCS tag/commit to use in the Python Whiteprint Git
            repository.
        exclude: user-chosen additional file exclusion patterns. Can be
            repeated to ignore multiple files.
        use_prereleases:Consider prereleases when detecting the latest one.
            Useless if specifying a `vcs_ref`.
        skip_if_exists: user-chosen additional file skip patterns. Can be
            repeated to ignore multiple files.
        cleanup_on_error: do NOT delete the destination DIRECTORY if there is
            an error.
        defaults: use default answers to questions, which might be null if not
            specified.
        overwrite: when set, overwrite files that already exist, without
            asking.
        pretend: when set, produce no real rendering.
        quiet: when set, disable all output.
        default_venv_backend: default virtual environment backend for Nox.
        skip_tests: skip tests after initializing the repository.
        data: user data used to answer questions.
        no_data: force not using `--data`.
        user_defaults: user defaults choices.
        python: force using the given python interpreter for the post
            processing.
        github_token: Github Token to push the newly created repository to
            Github. The token must have writing permissions.
        https_origin: force the origin to be an HTTPS URL.
    """
    data_dict = {} if no_data or data is None else read_yaml(data)
    data_dict.update(
        {
            "git_platform": (
                "no_git_platform" if github_token is None else "github"
            )
        }
    )
    user_defaults_dict = (
        {"project_name": destination.name}
        if user_defaults is None
        else read_yaml(user_defaults)
    )
    importlib.import_module("copier.main").Worker(
        src_path=src_path,
        dst_path=destination,
        answers_file=COPIER_ANSWER_FILE,
        vcs_ref=vcs_ref,
        data=data_dict,
        exclude=exclude,
        use_prereleases=use_prereleases,
        skip_if_exists=skip_if_exists,
        cleanup_on_error=cleanup_on_error,
        defaults=defaults,
        user_defaults=user_defaults_dict,
        overwrite=overwrite,
        pretend=pretend,
        quiet=quiet,
    ).run_copy()

    _post_processing(
        destination,
        default_venv_backend=default_venv_backend,
        skip_tests=skip_tests,
        python=python,
        github_token=github_token,
        https_origin=https_origin,
    )
