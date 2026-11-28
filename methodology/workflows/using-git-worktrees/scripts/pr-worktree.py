"""Track native Coacus worktrees and remove them after a verified PR delivery."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


OWNER_FILE = "coacus-worktree-owner"
OWNER_MARK = b"coacus-native-worktree-v1\n"
GIT_PATH_OVERRIDES = {"GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"}
ACTIVE_OPERATIONS = (
    "MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD",
    "rebase-merge", "rebase-apply", "sequencer", "BISECT_START", "index.lock",
)


class KeepWorktree(Exception):
    """A condition prevents safe automatic removal."""


def git(directory: Path, *args: str, input_data: bytes = b"", env: dict[str, str] | None = None) -> bytes:
    return subprocess.run(
        ["git", "-C", str(directory), *args],
        input=input_data, env=env, capture_output=True, check=True, timeout=30,
    ).stdout


def git_path(directory: Path, option: str) -> Path:
    output = git(directory, "rev-parse", "--path-format=absolute", option)
    return Path(os.fsdecode(output.removesuffix(b"\n"))).resolve()


def linked_git_dir(worktree: Path) -> Path:
    git_dir = git_path(worktree, "--git-dir")
    common_dir = git_path(worktree, "--git-common-dir")
    if (
        git_dir.parent != common_dir / "worktrees"
        or git_path(worktree, "--show-toplevel") != worktree
        or git(worktree, "rev-parse", "--show-superproject-working-tree").strip()
    ):
        raise KeepWorktree("the path is not the root of a native linked worktree")
    return git_dir


def registration(repository: Path, worktree: Path) -> dict[bytes, bytes]:
    output = git(repository, "worktree", "list", "--porcelain", "-z")
    for entry in output.split(b"\0\0"):
        fields = dict(field.partition(b" ")[::2] for field in entry.split(b"\0") if field)
        path = fields.get(b"worktree")
        if path and Path(os.fsdecode(path)).resolve() == worktree:
            return fields
    return {}


def mark(worktree: Path) -> None:
    owner = linked_git_dir(worktree) / OWNER_FILE
    try:
        with owner.open("xb") as stream:
            stream.write(OWNER_MARK)
    except FileExistsError:
        if owner.is_symlink() or owner.read_bytes() != OWNER_MARK:
            raise KeepWorktree("the ownership record is already in use") from None


def check_remote(worktree: Path, remote: str, head_ref: str, oid: bytes) -> None:
    try:
        push_urls = git(worktree, "remote", "get-url", "--push", "--all", "--", remote).splitlines()
        fetch_url = git(worktree, "remote", "get-url", "--", remote).removesuffix(b"\n")
        if push_urls != [fetch_url]:
            raise KeepWorktree("the push destination cannot be verified through the named remote")
        # Passing an expanded URL back to Git can apply insteadOf rules a second time.
        actual = git(worktree, "ls-remote", "--exit-code", "--refs", "--", remote, head_ref)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        raise KeepWorktree("the published branch could not be verified on the remote") from None
    if actual != oid + b"\t" + os.fsencode(head_ref) + b"\n":
        raise KeepWorktree("the remote branch differs from the confirmed PR commit")


def check_local(worktree: Path, git_dir: Path, head_ref: str, oid: bytes) -> None:
    if any((git_dir / name).exists() for name in ACTIVE_OPERATIONS):
        raise KeepWorktree("a Git operation is in progress")
    if (git_dir / "config.worktree").exists():
        raise KeepWorktree("the worktree has worktree-specific Git configuration")
    if git(worktree, "for-each-ref", "--format=%(refname)", "refs/worktree/", "refs/rewritten/", "refs/bisect/"):
        raise KeepWorktree("the worktree contains private Git refs")
    history = git(worktree, "reflog", "show", "--format=%H", "HEAD")
    if history and git(worktree, "rev-list", "--max-count=1", "--not", "--all", "--stdin", input_data=history):
        raise KeepWorktree("the checkout history contains commits without a ref")
    entries = git(worktree, "ls-files", "-v", "-z").split(b"\0")
    if any(entry[:1].islower() or entry.startswith(b"S ") for entry in entries):
        raise KeepWorktree("index flags can hide local changes")
    if git(worktree, "diff-index", "--cached", "--name-only", "-z", "--ignore-submodules=none", oid.decode("ascii"), "--"):
        raise KeepWorktree("local files contain staged changes")
    mode_check = ("-c", "core.filemode=true") if os.name != "nt" else ()
    # A new index has no cached file timestamps that could hide an edit.
    with tempfile.TemporaryDirectory(prefix="coacus-worktree-") as temporary:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temporary) / "index"))
        git(worktree, "-c", "core.sparseCheckout=false", "read-tree", oid.decode("ascii"), env=env)
        status = git(
            worktree, "-c", "core.fsmonitor=false", *mode_check,
            "status", "--porcelain=v1", "-z", "--untracked-files=all",
            "--ignored=matching", "--ignore-submodules=none", env=env,
        )
    if status:
        raise KeepWorktree("local files are modified, untracked, or ignored")
    if git(worktree, "symbolic-ref", "HEAD").rstrip(b"\n") != os.fsencode(head_ref):
        raise KeepWorktree("the worktree branch changed during cleanup")
    if git(worktree, "rev-parse", "HEAD").strip() != oid:
        raise KeepWorktree("the local commit changed during cleanup")


def cleanup(worktree: Path, repository: Path, remote: str, head_ref: str, head_oid: str) -> str:
    if repository.is_relative_to(worktree):
        raise KeepWorktree("run cleanup from outside the worktree")
    entry = registration(repository, worktree)
    if not entry:
        if not worktree.exists():
            return "Worktree already absent."
        raise KeepWorktree("the current repository does not register this worktree")
    if b"locked" in entry or b"prunable" in entry:
        raise KeepWorktree("the worktree is locked or its registration is stale")
    if not head_ref.startswith("refs/heads/") or entry.get(b"branch") != os.fsencode(head_ref):
        raise KeepWorktree("the worktree branch differs from the confirmed PR branch")
    oid = head_oid.encode("ascii")
    if entry.get(b"HEAD") != oid:
        raise KeepWorktree("the local commit differs from the confirmed PR commit")
    git_dir = linked_git_dir(worktree)
    owner = git_dir / OWNER_FILE
    if owner.is_symlink() or not owner.is_file() or owner.read_bytes() != OWNER_MARK:
        raise KeepWorktree("Coacus ownership could not be verified")
    check_remote(worktree, remote, head_ref, oid)
    check_local(worktree, git_dir, head_ref, oid)
    try:
        git(repository, "worktree", "remove", "--", str(worktree))
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        raise KeepWorktree("Git did not confirm removal; check the worktree before retrying") from None
    return "Worktree removed. Local and remote branches retained."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    mark_parser = actions.add_parser("mark", help="record a newly created native Coacus worktree")
    mark_parser.add_argument("worktree", type=Path)
    cleanup_parser = actions.add_parser("cleanup", help="remove the worktree after PR confirmation")
    cleanup_parser.add_argument("worktree", type=Path)
    cleanup_parser.add_argument("--remote", required=True)
    cleanup_parser.add_argument("--head-ref", required=True)
    cleanup_parser.add_argument("--head-oid", required=True)
    args = parser.parse_args()
    try:
        if GIT_PATH_OVERRIDES.intersection(os.environ):
            raise KeepWorktree("the Git environment overrides checkout or index paths")
        worktree = args.worktree.resolve()
        if args.action == "mark":
            mark(worktree)
            print("Coacus worktree ownership recorded.")
        else:
            print(cleanup(worktree, Path.cwd().resolve(), args.remote, args.head_ref, args.head_oid))
    except KeepWorktree as error:
        print(f"Worktree cleanup skipped: {error}.", file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        # Raw Git errors can contain paths, remote credentials, or local file names.
        print("Worktree action failed: Git or filesystem state could not be verified.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
