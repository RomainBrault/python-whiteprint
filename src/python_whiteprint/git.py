# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Git related functionalities."""

import logging
import pathlib
from typing import Final

import github
import pygit2
import yaml
from beartype import beartype
from beartype.typing import Iterable, Optional, Union


HEAD: Final = "HEAD"
"""Git HEAD ref."""

INITIAL_HEAD_NAME = "main"
"""Git default branch."""

WHITEPRINT_SIGNATURE: Final = pygit2.Signature(
    name="Python Whiteprint",
    email="1455095+RomainBrault@users.noreply.github.com",
)
"""Whiteprint Git signature for both authoring and commiting.

Note:
    we use a personal Git noreply email address for the moment.
"""


@beartype
def init_repository(destination: pathlib.Path) -> pygit2.repository.Repository:
    """Run git init.

    The default branch is named "main".

    Args:
        destination: the path of the Git repository.

    Returns:
        an empty Git repository.
    """
    return pygit2.init_repository(
        destination,
        initial_head=INITIAL_HEAD_NAME,
    )


@beartype
def git_add_all(
    repo: pygit2.repository.Repository,
) -> pygit2.Oid:
    """Run git add -A.

    Args:
        repo: a Git Repository.

    Returns:
        a Git Index.
    """
    repo.index.add_all()
    repo.index.write()
    return repo.index.write_tree()


@beartype
def add_and_commit(
    repo: pygit2.repository.Repository,
    *,
    message: str,
    ref: Optional[str] = None,
    author: pygit2.Signature = WHITEPRINT_SIGNATURE,
    committer: pygit2.Signature = WHITEPRINT_SIGNATURE,
    parents: Optional[Iterable[pygit2.Oid]] = None,
) -> None:
    """Run git add -A && git commit -m `message`.

    Args:
        repo: a Git Repository.
        message: a commit message.
        ref: an optional name of the reference to update. If none, use `HEAD`.
        author: an optional author.
        committer: an optional committer.
        parents: binary strings representing
            parents of the new commit. If none, use repository's head ref.
    """
    if ref is None:
        ref = repo.head.name

    if parents is None:
        parents = [repo.head.target]

    repo.create_commit(
        ref,
        author,
        committer,
        message,
        git_add_all(repo),
        list(parents),
    )


@beartype
def init_and_commit(
    destination: pathlib.Path,
    *,
    message: str = "chore: 🥇 inital commit.",
) -> pygit2.repository.Repository:
    """Run git init && git commmit -m `message`.

    Args:
        destination: the path of the Git repository.
        message: a commit message.

    Returns:
        a Git repository.
    """
    repo = init_repository(destination)
    add_and_commit(
        repo,
        message=message,
        author=WHITEPRINT_SIGNATURE,
        committer=WHITEPRINT_SIGNATURE,
        ref=HEAD,
        parents=[],
    )

    return repo


@beartype
def _find_entity(
    github_user: github.AuthenticatedUser.AuthenticatedUser,
    *,
    github_login: str,
) -> Union[
    github.AuthenticatedUser.AuthenticatedUser,
    github.Organization.Organization,
]:
    """Find and return an organization or user from the GitHub loging name.

    Args:
        github_user: an authenticated GitHub user.
        github_login: the GitHub login name of the user or the organization
            login.

    Returns:
        THe organization or user depending on the loging name.
    """
    organizations = [
        organization
        for organization in github_user.get_orgs()
        if organization.login == github_login
    ]
    return organizations[0] if len(organizations) == 1 else github_user


@beartype
def setup_github_repository(
    repo: pygit2.repository.Repository,
    *,
    project_slug: str,
    github_token: str,
    github_login: str,
    labels: pathlib.Path,
) -> None:
    """Create a repository on GitHub and push the local one.

    Args:
        repo: the local repository.
        project_slug: a slug of the project name.
        github_token: a GitHub token with repository write, delete, workflows
            and packages authorizations.
        github_login: the GitHub login name of the user or the organization
            login.
        labels: a path to a yaml file containing a list of labels with their
            descriptions.
    """
    github_user = github.Github(github_token, retry=3).get_user()

    github_repository = _find_entity(
        github_user, github_login=github_login
    ).create_repo(project_slug)

    repo.remotes.set_url(
        "origin",
        github_repository.clone_url,
    )
    repo.remotes.add_fetch("origin", "+refs/heads/*:refs/remotes/origin/*")

    logger = logging.getLogger(__name__)
    for label in yaml.safe_load(labels.read_text()):
        try:
            github_repository.create_label(**label)
        except github.GithubException as github_exception:
            logger.debug(github_exception)

    logger.debug("Pushing ref %s", repo.head.target)
    repo.remotes["origin"].push(
        [f"refs/heads/{INITIAL_HEAD_NAME}"],
        callbacks=pygit2.RemoteCallbacks(
            credentials=pygit2.UserPass("x-access-token", github_token)
        ),
    )


@beartype
def protect_repository(
    repo: pygit2.repository.Repository,
    *,
    project_slug: str,
    github_token: str,
    github_login: str,
    https_origin: bool,
) -> None:
    """Protect a Github repository.

    Args:
        repo: the local repository.
        project_slug: a slug of the project name (Repository to delete).
        github_token: a GitHub token with repository writing authorization.
        github_login: the GitHub login name of the user or the organization
            login.
        https_origin: force the origin to be an HTTPS URL.
    """
    github_user = github.Github(github_token, retry=3).get_user()
    github_repository = _find_entity(
        github_user, github_login=github_login
    ).get_repo(project_slug)

    branch = github_repository.get_branch(INITIAL_HEAD_NAME)
    branch.edit_protection(
        strict=True, enforce_admins=True, require_code_owner_reviews=True
    )

    # We do not test coverage here as it is too complex for little gains (e.g.
    # it requires the creation of an SSH key for the test session).
    if not https_origin:  # pragma: no cover
        repo.remotes.set_url(
            "origin",
            github_repository.ssh_url,
        )


def delete_github_repository(
    project_slug: str,
    *,
    github_token: str,
) -> None:
    """Delete a GitHub repository.

    Args:
        project_slug: a slug of the project name (Repository to delete).
        github_token: a GitHub token with repository writing authorization.
    """
    github_user = github.Github(github_token, retry=3).get_user()
    github_repository = github_user.get_repo(project_slug)
    github_repository.delete()
