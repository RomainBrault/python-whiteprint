# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

"""Git related functionalities."""

import pathlib
from typing import Final

import pygit2
from beartype import beartype
from beartype.typing import Iterable, Optional


HEAD: Final = "HEAD"
"""Git HEAD ref."""

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
        initial_head="main",
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
    message: str = "chore: inital commit.",
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
