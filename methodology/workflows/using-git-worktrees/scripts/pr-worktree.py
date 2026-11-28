"""Track native Coacus worktrees and remove them after a verified PR delivery."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path


OWNER_FILE = "coacus-worktree-owner"
OWNER_PREFIX = b"coacus-native-worktree-v2:"
RECOVERY_DIR = "coacus-worktree-recovery"
GIT_PATH_OVERRIDES = {"GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"}
RECOVERY_LOCK = "Coacus PR recovery"
INDEX_LOCK_PREFIX = b"coacus-pr-recovery:"
RECOVERY_LOCK_FILES = {"worktree-owner": "locked", "index-owner": "index.lock"}
ACTIVE_OPERATIONS = (
    "MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD",
    "MERGE_AUTOSTASH", "AUTO_MERGE", "rebase-merge", "rebase-apply",
    "sequencer", "BISECT_START",
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


def owner_id(git_dir: Path) -> str:
    owner = git_dir / OWNER_FILE
    if owner.is_symlink() or not owner.is_file():
        raise KeepWorktree("Coacus ownership could not be verified")
    record = owner.read_bytes()
    if record.startswith(OWNER_PREFIX):
        value = record[len(OWNER_PREFIX):].removesuffix(b"\n").decode("ascii")
        if len(value) == 32 and all(char in "0123456789abcdef" for char in value):
            return value
    raise KeepWorktree("Coacus ownership could not be verified for this worktree instance")


def mark(worktree: Path) -> None:
    git_dir = linked_git_dir(worktree)
    try:
        with (git_dir / OWNER_FILE).open("xb") as stream:
            stream.write(OWNER_PREFIX + uuid.uuid4().hex.encode("ascii") + b"\n")
    except FileExistsError:
        owner_id(git_dir)


def delivery_ticket(worktree: Path, remote: str) -> str:
    instance = owner_id(linked_git_dir(worktree))
    push_urls = git(worktree, "remote", "get-url", "--push", "--all", "--", remote).splitlines()
    fetch_url = git(worktree, "remote", "get-url", "--", remote).removesuffix(b"\n")
    if push_urls != [fetch_url]:
        raise KeepWorktree("the push destination cannot be verified through the named remote")
    return f"{instance}:{hashlib.sha256(fetch_url).hexdigest()}"


def check_ticket(worktree: Path, remote: str, expected: str) -> None:
    if delivery_ticket(worktree, remote) != expected:
        raise KeepWorktree("the worktree instance or remote changed since delivery was prepared")


def check_remote(worktree: Path, remote: str, head_ref: str, oid: bytes, ticket: str) -> None:
    try:
        check_ticket(worktree, remote, ticket)
        env = dict(os.environ, GIT_TERMINAL_PROMPT="0", SSH_ASKPASS_REQUIRE="never", GCM_INTERACTIVE="Never")
        env.pop("GIT_ASKPASS", None)
        # Passing an expanded URL back to Git can apply insteadOf rules a second time.
        actual = git(worktree, "-c", "core.askPass=", "ls-remote", "--exit-code", "--refs", "--", remote, head_ref, env=env)
        check_ticket(worktree, remote, ticket)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        raise KeepWorktree("the published branch could not be verified on the remote") from None
    if actual != oid + b"\t" + os.fsencode(head_ref) + b"\n":
        raise KeepWorktree("the remote branch differs from the confirmed PR commit")


def check_git_state(worktree: Path, git_dir: Path, oid: bytes) -> None:
    if any((git_dir / name).exists() for name in ACTIVE_OPERATIONS):
        raise KeepWorktree("a Git operation is in progress")
    if (git_dir / "config.worktree").exists():
        raise KeepWorktree("the worktree has worktree-specific Git configuration")
    if git(worktree, "for-each-ref", "--format=%(refname)", "refs/worktree/", "refs/rewritten/", "refs/bisect/"):
        raise KeepWorktree("the worktree contains private Git refs")
    history = git(worktree, "reflog", "show", "--format=%H", "HEAD")
    if (git_dir / "ORIG_HEAD").exists():
        history += git(worktree, "rev-parse", "--verify", "ORIG_HEAD^{commit}")
    fetch_head = git_dir / "FETCH_HEAD"
    if fetch_head.exists():
        history += b"".join(line.split(b"\t", 1)[0] + b"\n" for line in fetch_head.read_bytes().splitlines())
    if history and git(worktree, "rev-list", "--single-worktree", "--max-count=1", "--not", "--all", "--stdin", input_data=history):
        raise KeepWorktree("the checkout history contains commits without a ref")
    entries = git(worktree, "ls-files", "-v", "-z").split(b"\0")
    if any(entry[:1].islower() or entry.startswith(b"S ") for entry in entries):
        raise KeepWorktree("index flags can hide local changes")
    if git(worktree, "diff-index", "--cached", "--name-only", "-z", "--ignore-submodules=none", oid.decode("ascii"), "--"):
        raise KeepWorktree("local files contain staged changes")


def check_local(worktree: Path, git_dir: Path, oid: bytes) -> None:
    check_git_state(worktree, git_dir, oid)
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


def check_head(worktree: Path, head_ref: str, oid: bytes) -> None:
    if git(worktree, "symbolic-ref", "HEAD").rstrip(b"\n") != os.fsencode(head_ref):
        raise KeepWorktree("the worktree branch changed during cleanup")
    if git(worktree, "rev-parse", "HEAD").strip() != oid:
        raise KeepWorktree("the local commit changed during cleanup")


def recovery_root(repository: Path) -> Path:
    root = git_path(repository, "--git-common-dir") / RECOVERY_DIR
    if root.is_symlink():
        raise KeepWorktree("the recovery directory is a symbolic link")
    return root


def previous_recovery(repository: Path, ticket: str) -> Path | None:
    instance = ticket.partition(":")[0]
    if len(instance) == 32 and all(char in "0123456789abcdef" for char in instance):
        recovery = recovery_root(repository) / f"checkout-{instance}"
        if (recovery / "delivery.json").is_file():
            return recovery
    return None


def prepare_recovery(worktree: Path, git_dir: Path, repository: Path, head_ref: str, head_oid: str, instance: str) -> Path:
    root = recovery_root(repository)
    if root.is_relative_to(worktree):
        raise KeepWorktree("the recovery directory is inside this worktree")
    if owner_id(git_dir) != instance:
        raise KeepWorktree("the worktree instance changed before cleanup")
    root.mkdir(mode=0o700, exist_ok=True)
    recovery = root / f"checkout-{instance}"
    staging = Path(tempfile.mkdtemp(prefix="preparing-", dir=root))
    record = staging / "delivery.json"
    try:
        record.write_text(json.dumps({
            "worktree": str(worktree), "git_dir": git_dir.name, "owner": instance,
            "head_ref": head_ref, "head_oid": head_oid,
        }), encoding="utf-8")
        (staging / "worktree-owner").write_bytes(f"{RECOVERY_LOCK} {instance}\n".encode("ascii"))
        (staging / "index-owner").write_bytes(INDEX_LOCK_PREFIX + instance.encode("ascii"))
        staging.rename(recovery)
    except OSError:
        record.unlink(missing_ok=True)
        for name in RECOVERY_LOCK_FILES:
            (staging / name).unlink(missing_ok=True)
        staging.rmdir()
        raise KeepWorktree("the recovery record could not be written") from None
    return recovery


def archive(worktree: Path, git_dir: Path, recovery: Path, head_ref: str, oid: bytes) -> None:
    saved_checkout = recovery / "checkout"
    try:
        worktree.rename(saved_checkout)
        # Recheck Git state after moving the checkout. Keep the locked registration
        # if Git state changed. The lock protects its index from any later prune.
        check_head(saved_checkout, head_ref, oid)
        check_git_state(saved_checkout, git_dir, oid)
        (saved_checkout / ".git").rename(recovery / "git-link")
        git_dir.rename(recovery / "git-admin")
    except (OSError, KeepWorktree, subprocess.SubprocessError) as error:
        if not saved_checkout.exists():
            raise KeepWorktree("the checkout could not be moved into recovery") from None
        detail = f" ({error})" if isinstance(error, KeepWorktree) else ""
        raise KeepWorktree(f"checkout moved, but Git registration was not archived{detail}. Recover from {recovery}") from None


def finish_recovery(git_dir: Path, recovery: Path, *, restoring: bool = False) -> None:
    for name, filename in RECOVERY_LOCK_FILES.items():
        owner = recovery / name
        lock = git_dir / filename
        if lock.exists() or lock.is_symlink():
            if not lock.is_symlink() and owner.is_file() and lock.samefile(owner):
                lock.unlink()
            elif restoring:
                raise KeepWorktree(f"another Git operation holds a lock; recovery remains at {recovery}")
        owner.unlink(missing_ok=True)
    (recovery / "delivery.json").unlink()
    recovery.rmdir()


def restore(repository: Path, recovery: Path) -> None:
    root = recovery_root(repository)
    if recovery.parent != root:
        raise KeepWorktree("the recovery entry belongs to a different repository")
    data = json.loads((recovery / "delivery.json").read_text(encoding="utf-8"))
    worktree = Path(data["worktree"])
    admin_name = data["git_dir"]
    if not worktree.is_absolute() or Path(admin_name).name != admin_name or admin_name in {"", ".", ".."}:
        raise KeepWorktree("the recovery entry contains an invalid path")
    git_dir = root.parent / "worktrees" / admin_name
    saved_admin = recovery / "git-admin"
    saved_checkout = recovery / "checkout"
    saved_link = recovery / "git-link"
    ref = data["head_ref"]
    if worktree.is_dir() and not saved_checkout.exists() and not saved_admin.exists() and not saved_link.exists():
        if linked_git_dir(worktree) != git_dir or owner_id(git_dir) != data["owner"]:
            raise KeepWorktree("the original path belongs to a different worktree instance")
        finish_recovery(git_dir, recovery, restoring=True)
        return
    if worktree.exists() or worktree.is_symlink() or not saved_checkout.is_dir():
        raise KeepWorktree("the original path is occupied or the saved checkout is unavailable")
    registered = git(repository, "worktree", "list", "--porcelain", "-z").split(b"\0\0")
    branch = b"branch " + os.fsencode(ref)
    for entry in registered:
        fields = entry.split(b"\0")
        if branch in fields and fields[0] != b"worktree " + os.fsencode(worktree):
            raise KeepWorktree("the branch is in use by another checkout")
    if not ref.startswith("refs/heads/") or (
        git(repository, "rev-parse", "--verify", "--end-of-options", ref).strip() != data["head_oid"].encode("ascii")
    ):
        raise KeepWorktree("the branch has moved since cleanup")
    archived = saved_admin.is_dir()
    if owner_id(saved_admin if archived else git_dir) != data["owner"]:
        raise KeepWorktree("recovery metadata belongs to a different worktree instance")
    if archived:
        if git_dir.exists() or git_dir.is_symlink():
            raise KeepWorktree("the original Git registration is occupied")
        git_dir.parent.mkdir(exist_ok=True)
        saved_admin.rename(git_dir)
    try:
        if saved_link.is_file():
            saved_link.rename(saved_checkout / ".git")
        saved_checkout.rename(worktree)
    except OSError:
        raise KeepWorktree(f"checkout restore incomplete; recover from {recovery}") from None
    finish_recovery(git_dir, recovery, restoring=True)


def cleanup(worktree: Path, repository: Path, remote: str, head_ref: str, head_oid: str, ticket: str) -> str:
    if repository.is_relative_to(worktree):
        raise KeepWorktree("run cleanup from outside the worktree")
    entry = registration(repository, worktree)
    if not entry:
        if not worktree.exists():
            recovery = previous_recovery(repository, ticket)
            if recovery:
                return f"Worktree already absent. Recovery copy: {recovery}"
            return "Worktree already absent."
        raise KeepWorktree("the current repository does not register this worktree")
    if b"locked" in entry or b"prunable" in entry:
        recovery = previous_recovery(repository, ticket)
        if recovery:
            raise KeepWorktree(f"the checkout has a recovery copy at {recovery}")
        raise KeepWorktree("the worktree is locked or its registration is stale")
    if not head_ref.startswith("refs/heads/") or entry.get(b"branch") != os.fsencode(head_ref):
        raise KeepWorktree("the worktree branch differs from the confirmed PR branch")
    oid = head_oid.encode("ascii")
    if entry.get(b"HEAD") != oid:
        raise KeepWorktree("the local commit differs from the confirmed PR commit")
    git_dir = linked_git_dir(worktree)
    if git_dir.parent != git_path(repository, "--git-common-dir") / "worktrees":
        raise KeepWorktree("the checkout belongs to a different repository")
    check_ticket(worktree, remote, ticket)
    check_local(worktree, git_dir, oid)
    check_remote(worktree, remote, head_ref, oid, ticket)
    instance = ticket.partition(":")[0]
    recovery = prepare_recovery(worktree, git_dir, repository, head_ref, head_oid, instance)
    try:
        try:
            # A prewritten exclusive hard link is never visible as an empty lock.
            for name, filename in RECOVERY_LOCK_FILES.items():
                os.link(recovery / name, git_dir / filename)
        except FileExistsError:
            raise KeepWorktree("the worktree is locked or a Git operation is in progress") from None
        except OSError:
            raise KeepWorktree("the filesystem could not install exclusive recovery locks") from None
        check_head(worktree, head_ref, oid)
        archive(worktree, git_dir, recovery, head_ref, oid)
    finally:
        if worktree.is_dir() and not (recovery / "checkout").exists():
            finish_recovery(git_dir, recovery)
    return f"Worktree removed from the active checkouts. Recovery copy: {recovery}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    mark_parser = actions.add_parser("mark", help="record a newly created native Coacus worktree")
    mark_parser.add_argument("worktree", type=Path)
    prepare_parser = actions.add_parser("prepare", help="capture the worktree instance and push destination before delivery")
    prepare_parser.add_argument("worktree", type=Path)
    prepare_parser.add_argument("--remote", required=True)
    cleanup_parser = actions.add_parser("cleanup", help="remove the worktree after PR confirmation")
    cleanup_parser.add_argument("worktree", type=Path)
    cleanup_parser.add_argument("--remote", required=True)
    cleanup_parser.add_argument("--head-ref", required=True)
    cleanup_parser.add_argument("--head-oid", required=True)
    cleanup_parser.add_argument("--ticket", required=True)
    restore_parser = actions.add_parser("restore", help="restore a checkout from its recovery entry")
    restore_parser.add_argument("worktree", type=Path, metavar="recovery")
    args = parser.parse_args()
    try:
        if GIT_PATH_OVERRIDES.intersection(os.environ):
            raise KeepWorktree("the Git environment overrides checkout or index paths")
        worktree = args.worktree.resolve()
        if args.action == "mark":
            mark(worktree)
            print("Coacus worktree ownership recorded.")
        elif args.action == "prepare":
            print(delivery_ticket(worktree, args.remote))
        elif args.action == "restore":
            restore(Path.cwd().resolve(), worktree)
            print("Worktree restored.")
        else:
            print(cleanup(worktree, Path.cwd().resolve(), args.remote, args.head_ref, args.head_oid, args.ticket))
    except KeepWorktree as error:
        print(f"Worktree cleanup skipped: {error}.", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError):
        # Raw Git errors can contain paths, remote credentials, or local file names.
        print("Worktree action failed: Git or filesystem state could not be verified.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
