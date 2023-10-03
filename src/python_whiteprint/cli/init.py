# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Initialize a new Python project."""

import importlib
import logging
import shutil
from pathlib import Path
from typing import Final

from beartype.typing import (
    Any,
    Dict,
    List,
    Optional,
)
from click import core
from returns.maybe import Maybe
from typer import params
from typing_extensions import Annotated, TypeGuard

from python_whiteprint.cli.environment import DEFAULTS
from python_whiteprint.cli.exceptions import (
    NotAValidYAMLError,
    UnsupportedTypeInMappingError,
)
from python_whiteprint.cli.types import DefaultVenvBackend, Yaml
from python_whiteprint.loc import _


__all__: Final = [
    "YAML_EXT",
    "COPIER_ANSWER_FILE",
    "LABEL_FILE",
    "read_yaml",
    "autocomplete_yaml_file",
    "init",
]
"""Public module attributes."""


YAML_EXT: Final = [".yaml", ".yml"]
COPIER_ANSWER_FILE: Final = ".copier-answers.yml"
LABEL_FILE: Final = ".github/labels.yml"


def read_yaml(data: Path) -> Yaml:
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
            raise NotAValidYAMLError(data, str(parser_error)) from parser_error

        if _check_dict(copier_data):
            return copier_data

    raise UnsupportedTypeInMappingError


def _copy_license_to_project_root(destination: Path) -> None:
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


def _format_code(
    destination: Path,
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
    try:  # pragma: no cover
        nox.run(
            destination=destination,
            args=[
                "--default-venv-backend",
                default_venv_backend.value.lower(),
                *(
                    Maybe.from_optional(python)
                    .map(lambda _python: ("--force-python", _python))
                    .value_or(())
                ),
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


def _download_licenses(
    destination: Path,
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
            *(
                Maybe.from_optional(python)
                .map(lambda _python: ("--force-python", _python))
                .value_or(())
            ),
            "--session",
            "reuse",
            "--",
            "download",
            "--all",
        ],
    )

    _copy_license_to_project_root(destination)


def _post_processing(
    destination: Path,
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
    github = importlib.import_module("github")

    # Create poetry.lock
    poetry.robust_lock(destination)

    repository = git.init_and_commit(destination)

    # Download the required licenses.
    _download_licenses(
        destination, default_venv_backend=default_venv_backend, python=python
    )
    git.add_and_commit(repository, message="chore: 📃 download license(s).")

    force_python = (
        Maybe.from_optional(python)
        .map(lambda _python: ("--force-python", _python))
        .value_or(())
    )
    # Generate the dependencies table.
    nox.run(
        destination=destination,
        args=[
            "--default-venv-backend",
            default_venv_backend.value.lower(),
            *force_python,
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
                *force_python,
            ],
        )

    if (
        token := Maybe.from_optional(github_token)
        .map(github.Auth.Token)
        .value_or(False)
    ):
        copier_answers = read_yaml(destination / COPIER_ANSWER_FILE)
        git.setup_github_repository(
            repository,
            project_slug=copier_answers["project_slug"],
            token=token,
            login=copier_answers["github_user"],
            labels=destination / LABEL_FILE,
        )
        git.protect_repository(
            repository,
            project_slug=copier_answers["project_slug"],
            token=token,
            login=copier_answers["github_user"],
            https_origin=https_origin,
        )


def _autocomplete_suffix(incomplete: Path) -> List[str]:
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
    path = Path(incomplete)
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


def _check_dict(data: Dict[str, Any]) -> TypeGuard[Yaml]:
    """Check if the values type of a given dictionary are strings or integers.

    Args:
        data: the dictionary to check:

    Returns:
        a boolean (type guard) indicating whether the values are all strings or
        integers.
    """
    return all(isinstance(v, (str, int)) for v in data.values())


def init(  # pylint: disable=too-many-locals
    *,
    destination: Annotated[
        Path,
        params.Argument(
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
            readable=False,
            resolve_path=True,
            metavar="DIRECTORY",
            help=_("Destination path where to create the Python project."),
        ),
    ] = Path(),
    src_path: Annotated[
        str,
        params.Option(
            "--whiteprint-source",
            "-w",
            envvar="WHITEPRINT_REPOSITORY",
            help=_(
                "The location of the Python Whiteprint Git repository (string"
                " that"
                " can be resolved to a template path, be it local or remote)."
            ),
        ),
    ] = DEFAULTS.copier.repository,
    vcs_ref: Annotated[
        Optional[str],
        params.Option(
            "--vcs-ref",
            "-v",
            envvar="WHITEPRINT_VCS_REF",
            help=_(
                "Specify the VCS tag/commit to use in the Python"
                " Whiteprint Git"
                " repository."
            ),
        ),
    ] = DEFAULTS.copier.vcs_ref,
    exclude: Annotated[
        Optional[List[str]],
        params.Option(
            "--exclude",
            "-x",
            help=_(
                "User-chosen additional file exclusion patterns. Can be"
                " repeated to ignore multiple files."
            ),
        ),
    ] = None,
    use_prereleases: Annotated[
        bool,
        params.Option(
            "--use-prereleases",
            "-P",
            help=_(
                "Consider prereleases when detecting the latest one."
                " Useless if specifying a --vcs-ref."
            ),
        ),
    ] = False,
    skip_if_exists: Annotated[
        Optional[List[str]],
        params.Option(
            "--skip-if-exsists",
            "-s",
            help=_(
                "User-chosen additional file skip patterns. Can be repeated to"
                " ignore multiple files."
            ),
        ),
    ] = None,
    cleanup_on_error: Annotated[
        bool,
        params.Option(
            "--no-cleanup-on-error",
            "-C",
            help=_(
                "Do NOT delete the destination DIRECTORY if there is an error."
            ),
        ),
    ] = False,
    defaults: Annotated[
        bool,
        params.Option(
            "--defaults",
            "-D",
            help=_(
                "Use default answers to questions, which might be null if not"
                " specified."
            ),
        ),
    ] = False,
    overwrite: Annotated[
        bool,
        params.Option(
            "--overwrite",
            "-O",
            help=_(
                "When set, overwrite files that already exist, without asking."
            ),
        ),
    ] = False,
    pretend: Annotated[
        bool,
        params.Option(
            "--pretend",
            "-P",
            help=_("When set, produce no real rendering."),
        ),
    ] = False,
    quiet: Annotated[
        bool,
        params.Option(
            "--quiet",
            "-Q",
            help=_("When set, disable all output."),
        ),
    ] = False,
    default_venv_backend: Annotated[
        DefaultVenvBackend,
        params.Option(
            "--default-venv-backend",
            "-b",
            case_sensitive=False,
            envvar="WHITEPRINT_DEFAULT_VENV_BACKEND",
            help=_("Default virtual environment backend for Nox."),
        ),
    ] = DEFAULTS.post_processing.default_venv_backend,
    skip_tests: Annotated[
        bool,
        params.Option(
            "--skip-tests",
            "-S",
            envvar="WHITEPRINT_SKIP_TESTS",
            help=_("Skip tests after initializing the repository."),
        ),
    ] = DEFAULTS.post_processing.skip_tests,
    data: Annotated[
        Path,
        params.Option(
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
        ),
    ] = DEFAULTS.copier.data,
    no_data: Annotated[
        bool,
        params.Option(
            "--no-data",
            "-n",
            help=_("Force not using --data."),
        ),
    ] = False,
    user_defaults: Annotated[
        Optional[Path],
        params.Option(
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
        ),
    ] = DEFAULTS.copier.user_defaults,
    python: Annotated[
        Optional[str],
        params.Option(
            "--python",
            "-p",
            envvar="WHITEPRINT_PYTHON",
            help=_(
                "force using the given python interpreter for the post"
                " processing."
            ),
        ),
    ] = DEFAULTS.post_processing.python,
    github_token: Annotated[
        Optional[str],
        params.Option(
            "--github-token",
            help=_(
                "Github Token to push the newly created repository to"
                " Github. The"
                " token must have writing permissions."
            ),
            envvar="WHITEPRINT_GITHUB_TOKEN",
        ),
    ] = DEFAULTS.post_processing.github_token,
    https_origin: Annotated[
        bool,
        params.Option(
            "--https-origin",
            "-H",
            envvar="WHITEPRINT_HTTPS_ORIGIN",
            help=_("Force the origin to be an https URL."),
        ),
    ] = DEFAULTS.post_processing.https_origin,
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
    data_dict: Yaml = (
        {}
        if no_data
        else Maybe.from_optional(data).map(read_yaml).value_or({})
    )
    data_dict.update(
        {
            "git_platform": (
                Maybe.from_optional(github_token)
                .map(lambda _token: "github")
                .value_or("no_git_platform")
            )
        }
    )
    user_defaults_dict = (
        Maybe.from_optional(user_defaults)
        .map(read_yaml)
        .value_or({"project_name": destination.name})
    )
    importlib.import_module("copier.main").Worker(
        src_path=src_path,
        dst_path=destination,
        answers_file=COPIER_ANSWER_FILE,
        vcs_ref=vcs_ref,
        data=data_dict,
        exclude=Maybe.from_optional(exclude).value_or([]),
        use_prereleases=use_prereleases,
        skip_if_exists=Maybe.from_optional(skip_if_exists).value_or([]),
        cleanup_on_error=cleanup_on_error,
        defaults=defaults,
        user_defaults=user_defaults_dict,
        overwrite=overwrite,
        pretend=pretend,
        quiet=quiet,
        unsafe=True,
    ).run_copy()

    _post_processing(
        destination,
        default_venv_backend=default_venv_backend,
        skip_tests=skip_tests,
        python=python,
        github_token=github_token,
        https_origin=https_origin,
    )
