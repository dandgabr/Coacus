"""The end-of-session improvement loop (F10).

Runs the pipeline once per invocation: capture → consolidate → route → verify →
stage. It is opt-in, fail-open, and NEVER applies a change (D7): the output is a
runtime proposal ledger entry plus a reviewable staging bundle.

Review references contain a random run identifier and 1-based positions among
accepted JSON objects. A private association retains a source snapshot and exact
proposal references. Routing metadata can reveal information.

The loop is intentionally not imported by ``generate``/``check``: a test asserts
``engine.improve`` is absent from ``sys.modules`` after those commands, so the
non-deterministic subsystem cannot leak into the deterministic build contract.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import stat
import tempfile
import uuid
from pathlib import Path

from engine.improve import consolidate, ledger, route as router, sources, verify

STAGING = "docs/temp/improvement"
# ponytail: cap snapshots at 10 MiB; use streaming ingestion if larger inputs are needed.
MAX_SOURCE_BYTES = 10 * 1024 * 1024


def _windows() -> bool:
    return os.name == "nt"


def _read_source(path: Path) -> bytes:
    if os.name == "posix":
        if not hasattr(os, "O_NONBLOCK"):
            raise OSError("safe source opening unavailable")
        stream = os.fdopen(os.open(path, os.O_RDONLY | os.O_NONBLOCK), "rb")
    else:
        stream = path.open("rb")
    with stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_SOURCE_BYTES:
            raise ValueError("source is not a regular file or exceeds size limit")
        data = stream.read(MAX_SOURCE_BYTES + 1)
        if len(data) > MAX_SOURCE_BYTES:
            raise ValueError("source exceeds size limit")
        return data


def _alarm_for(statuses: dict[str, str]) -> list[str]:
    """Absent-by-config is a safe skip; absent-unexpectedly is an alarm."""
    return [
        f"source {name!r} is configured but unreachable — improvement auditing is degraded"
        for name, status in statuses.items()
        if status == "absent_unexpectedly"
    ]


def _private_dir(root: Path) -> Path:
    """Use owner-only POSIX storage; refuse platforms without these guarantees."""
    if os.name != "posix":
        raise OSError("private proposal storage requires POSIX permissions")
    path = root / ".ai-memory" / "improve-sources"
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.mkdir(mode=0o700, exist_ok=True)
    for directory, forbidden in ((path.parent, 0o022), (path, 0o077)):
        info = directory.lstat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & forbidden or info.st_mode & 0o700 != 0o700):
            raise OSError("private proposal directory is not secure")
    return path


def _save_source(root: Path, run_id: str, name: str, data: bytes, proposals: list[dict]) -> None:
    directory = _private_dir(root)
    path = directory / (run_id + ".json")
    if not hasattr(os, "O_NOFOLLOW"):
        raise OSError("safe private association creation unavailable")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o600:
                raise OSError("private association permissions are unusable")
            json.dump({"source": name, "snapshot": data.decode("utf-8"),
                       "reviews": [p["review"] for p in proposals], "proposals": proposals}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        entry = _load_source(root, run_id)
        reviews = [p["review"] for p in proposals]
        if entry != {"source": name, "snapshot": data.decode("utf-8"), "reviews": reviews, "proposals": proposals}:
            raise ValueError("private association mismatch")
        observations = sources.parse_observations(entry["snapshot"])
        for review in reviews:
            _evidence(observations, review)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        path.unlink(missing_ok=True)
        raise ValueError("private association unavailable or invalid") from exc


def _load_source(root: Path, run_id: str) -> dict:
    if not isinstance(run_id, str) or len(run_id) != 32 or any(c not in "0123456789abcdef" for c in run_id):
        raise ValueError("invalid run identifier")
    path = _private_dir(root) / (run_id + ".json")
    if not hasattr(os, "O_NONBLOCK") or not hasattr(os, "O_NOFOLLOW"):
        raise OSError("safe private association opening unavailable")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, encoding="utf-8") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise ValueError("insecure private association")
        return json.load(stream)


def _evidence(observations: list[dict], review: dict) -> list[dict]:
    indexes = review["observation_indexes"]
    if not isinstance(indexes, list) or not indexes or any(type(i) is not int or i < 1 or i > len(observations) for i in indexes):
        raise ValueError("invalid observation indexes")
    return [observations[i - 1] for i in indexes]


def recover(root: Path, review: dict, source_path: Path | None = None, recovery_key: str | None = None) -> list[dict]:
    """Recover evidence; review-only references are accepted only for legacy snapshots."""
    try:
        proposal = review
        review = proposal.get("review", proposal)
        if review.get("source_locator") == "user-supplied":
            if source_path is None or recovery_key is None or proposal is review:
                raise ValueError("original source, complete proposal and recovery key required")
            key = bytes.fromhex(recovery_key)
            if len(key) != 32:
                raise ValueError("invalid recovery key")
            data = _read_source(Path(source_path))
            reference = {**proposal, "review": {k: v for k, v in review.items() if k != "verifier"}}
            message = json.dumps(reference, sort_keys=True, separators=(",", ":")).encode() + b"\0" + data
            if not hmac.compare_digest(hmac.new(key, message, hashlib.sha256).hexdigest(), review["verifier"]):
                raise ValueError("source or proposal reference mismatch")
            return _evidence(sources.parse_observations(data.decode("utf-8")), review)
        entry = _load_source(root, review["run_id"])
        if entry["source"] != review["source"] or review not in entry["reviews"]:
            raise ValueError("proposal reference mismatch")
        if proposal is review and "proposals" in entry:
            raise ValueError("complete proposal required")
        if proposal is not review:
            encoded = json.dumps(proposal, sort_keys=True, separators=(",", ":"))
            if not any(encoded == json.dumps(saved, sort_keys=True, separators=(",", ":"))
                       for saved in entry.get("proposals", [])):
                raise ValueError("complete proposal authentication unavailable or mismatch")
        return _evidence(sources.parse_observations(entry["snapshot"]), review)
    except (OSError, KeyError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("private source unavailable or invalid") from exc


def run(root: Path, options: dict, registry: sources.SourceRegistry | None = None) -> dict:
    """Execute the pipeline with the supplied registry or the built-in sources."""
    if registry is None:
        registry = sources.SourceRegistry()
        sources.register_builtin(registry)
    requested = options.get("source") or "transcript"
    source = registry.get(requested)
    if source is None:
        return {"ok": False, "reason": f"unknown source {requested!r}", "proposals": []}

    statuses = {}
    failed_statuses = set()
    for name in registry.names():
        try:
            statuses[name] = registry.get(name).status(root)
        except Exception:
            statuses[name] = "absent_unexpectedly"
            failed_statuses.add(name)
    alarms = _alarm_for(statuses)
    if requested in failed_statuses:
        return {"ok": False, "reason": "source unavailable or invalid", "alarms": alarms, "proposals": []}

    from engine.improve.sources.ai_memory import AiMemorySource
    from engine.improve.sources.transcript import TranscriptSource

    key = {TranscriptSource: "transcript", AiMemorySource: "memory_export"}.get(type(source))
    raw_path = options.get(key) if key else None
    if raw_path is not None and not _windows() and (os.name != "posix" or not hasattr(os, "O_NONBLOCK") or not hasattr(os, "O_NOFOLLOW")):
        return {"ok": False, "reason": "source processing unavailable on unsupported platform", "alarms": alarms, "proposals": []}
    try:
        if raw_path is not None and not raw_path:
            raise ValueError("empty source")
        source_path = Path(raw_path).resolve(strict=True) if raw_path is not None else None
        data = b""
        if source_path and _windows():
            data = _read_source(source_path)
        elif source_path:
            fd = os.open(source_path, os.O_RDONLY | os.O_NONBLOCK)
            with os.fdopen(fd, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_SOURCE_BYTES:
                    raise ValueError("source is not a regular file or exceeds size limit")
                data = stream.read(MAX_SOURCE_BYTES + 1)
                if len(data) > MAX_SOURCE_BYTES:
                    raise ValueError("source exceeds size limit")
        if key is None:
            if _windows():
                raise ValueError("custom sources require private snapshot storage")
            try:
                observations = source.read(root, options)
            except Exception:
                return {"ok": False, "reason": "source unavailable or invalid", "alarms": alarms, "proposals": []}
            if not isinstance(observations, list) or any(not isinstance(item, dict) for item in observations):
                raise ValueError("source must return a list of observation objects")
            data = ("\n".join(json.dumps(item, ensure_ascii=False, allow_nan=False) for item in observations)).encode("utf-8")
            if len(data) > MAX_SOURCE_BYTES or sources.parse_observations(data.decode("utf-8")) != observations:
                raise ValueError("source observations cannot be recovered faithfully")
        else:
            observations = sources.parse_observations(data.decode("utf-8"))
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError):
        return {"ok": False, "reason": "source unavailable or invalid", "alarms": alarms, "proposals": []}
    if not observations:
        return {
            "ok": True,
            "status": statuses[requested],
            "alarms": alarms,
            "proposals": [],
            "note": "no observations available — fail-open no-op",
        }

    try:
        candidates = consolidate.consolidate(observations)
    except UnicodeError:
        return {"ok": False, "reason": "source unavailable or invalid", "alarms": alarms, "proposals": []}
    run_id = uuid.uuid4().hex
    proposals: list[dict] = []
    for candidate in candidates:
        # Taint rule: a rule/procedure needs trusted evidence; else it is a note.
        if candidate["type"] in ("gotcha", "procedure") and not candidate["trusted"]:
            candidate["type"] = "note"
            candidate["downgraded"] = "externally-tainted evidence"

        routing = router.route(root, candidate)
        if routing["decision"] == "skip":
            continue
        result = verify.verify(root, candidate, routing)
        if not result["passed"]:
            continue
        record = {
            "type": candidate["type"],
            # Free-form observations cannot be reliably classified as non-sensitive.
            # Hashes of short claims also permit offline guessing.
            "statement": "[observation withheld]",
            "review": {
                "source": requested,
                "run_id": run_id,
                "source_locator": "private",
                "observation_indexes": [e["observation_index"] for e in candidate["evidence"]],
            },

            "support": candidate.get("support", 0),
            "trusted": candidate.get("trusted", False),
            "routing": routing,
            "verification": result,
            "status": "proposed",
        }
        proposals.append(record)

    if proposals and _windows():
        try:
            key = bytes.fromhex(os.environ.get("COACUS_IMPROVE_RECOVERY_KEY", ""))
            if len(key) != 32:
                raise ValueError("invalid key")
        except ValueError:
            return {"ok": False, "reason": "operator recovery key unavailable or invalid", "alarms": alarms, "proposals": []}
        for record in proposals:
            review = record["review"]
            review["source_locator"] = "user-supplied"
            message = json.dumps(record, sort_keys=True, separators=(",", ":")).encode() + b"\0" + data
            review["verifier"] = hmac.new(key, message, hashlib.sha256).hexdigest()
    elif proposals:
        try:
            _save_source(root, run_id, requested, data, proposals)
        except (OSError, ValueError):
            return {"ok": False, "reason": "private source association unavailable", "alarms": alarms, "proposals": []}
    published: list[dict] = []
    attempted: list[dict] = []
    temporary = None
    try:
        for record in proposals:
            attempted.append(record)
            ledger.append_runtime(root, record)
            published.append(record)

        staging = root / STAGING
        staging.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=staging,
                                         suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps({"proposals": proposals, "alarms": alarms}, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, staging / "last-run.json")
    except OSError:
        return {"ok": False, "reason": "proposal publication incomplete", "publication_status": "uncertain",
                "reconciliation": attempted, "alarms": alarms, "proposals": published}
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
    return {
        "ok": True,
        "status": statuses[requested],
        "alarms": alarms,
        "proposals": proposals,
    }
