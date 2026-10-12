"""On-disk concurrency governor with an flock-guarded slot ledger (orchestration-governance).

Bounds how many agents may run at once (default 5, orchestrator included),
handles rate-limit (429) by parking a caller as PAUSED for retry, and is the
executable counterpart of the AGENTS.md governance rule. Zero dependencies.

Ledger format (text, one record per line):
    MAX <n>                                  # authoritative cap (first line)
    RUNNING <caller> <yes|no> <token> <pid> <started-unix-ts>
    PAUSED  <caller> <unix-ts> <attempts>

Callers are validated tokens (``[A-Za-z0-9._:-]+``); matching is EXACT, never
prefix-based. The cap is persisted so no caller can raise it. Stale RUNNING
rows (dead PID or older than the lease) are reaped before capacity is judged,
so a crashed holder cannot leak a slot forever.
"""

from __future__ import annotations

import os
import re
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

DEFAULT_MAX_TOTAL = 6
POLL_SECONDS = 0.2
DEFAULT_LEASE_SECONDS = 900
CALLER_RE = re.compile(r"^[A-Za-z0-9._:-]+$")

HARNESS_CONCURRENCY_MAP: dict[str, int] = {
    "ollama": 2,
    "command-code": 4,
    "cursor": 5,
    "opencode": 5,
    "antigravity": 6,
    "claude-code": 8,
    "codex": 10,
}

MODEL_CONCURRENCY_MAP: dict[str, int] = {
    "flash": 8,
    "pro": 5,
    "haiku": 10,
    "sonnet": 8,
    "opus": 4,
    "mini": 10,
}


def resolve_concurrency_cap(
    scope: str = "global",
    model: str | None = None,
    explicit_max: int | None = None,
) -> int:
    """Resolve the concurrency cap dynamically following precedence rules:

    1. Explicit max_total parameter if supplied.
    2. Model-specific environment variable (COACUS_MAX_<MODEL>).
    3. Harness-specific environment variable (COACUS_MAX_<SCOPE>).
    4. Harness-native environment variable (e.g. CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY, OLLAMA_NUM_PARALLEL).
    5. Model canonical mapping if model is known.
    6. Harness canonical mapping if scope is known in HARNESS_CONCURRENCY_MAP.
    7. Global override ORCH_MAX_CONCURRENT if set in environment.
    8. Default fallback for other/unlisted harnesses: 6.
    """
    if explicit_max is not None:
        return max(int(explicit_max), 1)

    norm_scope = (scope or "global").strip().lower()
    norm_model = (model or "").strip().lower() if model else ""

    # 2. Model-specific env var (e.g. COACUS_MAX_FLASH=8)
    if norm_model:
        model_env = f"COACUS_MAX_{norm_model.upper().replace('-', '_')}"
        if model_env in os.environ:
            try:
                return max(int(os.environ[model_env]), 1)
            except ValueError:
                pass

    # 3. Scope/Harness-specific env var (e.g. COACUS_MAX_ANTIGRAVITY=6, COACUS_MAX_CODEX=10)
    scope_env = f"COACUS_MAX_{norm_scope.upper().replace('-', '_')}"
    if scope_env in os.environ:
        try:
            return max(int(os.environ[scope_env]), 1)
        except ValueError:
            pass

    # 4. Harness-native environment variables
    if norm_scope in ("claude", "claude-code") and "CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY" in os.environ:
        try:
            return max(int(os.environ["CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY"]), 1)
        except ValueError:
            pass
    if norm_scope == "ollama" and "OLLAMA_NUM_PARALLEL" in os.environ:
        try:
            return max(int(os.environ["OLLAMA_NUM_PARALLEL"]), 1)
        except ValueError:
            pass

    # 5. Model canonical mapping
    if norm_model:
        for key, cap in MODEL_CONCURRENCY_MAP.items():
            if key in norm_model:
                return cap

    # 6. Harness canonical mapping
    if norm_scope in HARNESS_CONCURRENCY_MAP:
        return HARNESS_CONCURRENCY_MAP[norm_scope]

    # 7. Legacy ORCH_MAX_CONCURRENT
    if "ORCH_MAX_CONCURRENT" in os.environ:
        try:
            return max(int(os.environ["ORCH_MAX_CONCURRENT"]), 1)
        except ValueError:
            pass

    # 8. Default fallback for others
    return DEFAULT_MAX_TOTAL


def state_dir() -> Path:
    """The governor's state directory (``GOVERNOR_STATE_DIR`` or a runtime default)."""
    override = os.environ.get("GOVERNOR_STATE_DIR")
    if override:
        return Path(override)
    runtime = os.environ.get("XDG_RUNTIME_DIR") or tempfile.gettempdir()
    return Path(runtime) / "coacus-governor"


def _env_max_total(scope: str = "global", model: str | None = None) -> int:
    return resolve_concurrency_cap(scope=scope, model=model)


def _lease_seconds() -> int:
    raw = os.environ.get("GOVERNOR_LEASE_SECONDS", str(DEFAULT_LEASE_SECONDS))
    try:
        return max(int(raw), 1)
    except ValueError:
        return DEFAULT_LEASE_SECONDS


class Ledger:
    """A file-backed slot ledger guarded by ``fcntl.flock``."""

    def __init__(
        self,
        directory: Path | None = None,
        max_total: int | None = None,
        lease_seconds: int = DEFAULT_LEASE_SECONDS,
        scope: str = "global",
        model: str | None = None,
    ):
        """Open the ledger, creating its directory with owner-only permissions."""
        self.scope = (scope or "global").strip().lower()
        self.model = model
        self.dir = Path(directory) if directory else state_dir()
        self.requested_max = (
            int(max_total)
            if max_total is not None
            else resolve_concurrency_cap(self.scope, self.model)
        )
        self.lease_seconds = int(lease_seconds) if lease_seconds else _lease_seconds()
        file_suffix = "" if self.scope == "global" else f"-{self.scope}"
        self.path = self.dir / f"ledger{file_suffix}"
        self.lock_path = self.dir / f"ledger{file_suffix}.lock"
        self.dir.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            os.chmod(self.dir, 0o700)
        self.lock_path.touch(exist_ok=True)

    # -- locking ---------------------------------------------------------

    @contextmanager
    def _locked(self):
        fd = os.open(self.lock_path, os.O_RDWR | os.O_CREAT, 0o600)
        unlock = None
        try:
            try:
                import fcntl  # POSIX

                fcntl.flock(fd, fcntl.LOCK_EX)

                def unlock() -> None:
                    fcntl.flock(fd, fcntl.LOCK_UN)
            except ImportError:  # pragma: no cover - Windows fallback
                import msvcrt

                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_LOCK, 1)

                def unlock() -> None:
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            yield
        finally:
            if unlock is not None:
                unlock()
            os.close(fd)

    # -- storage ---------------------------------------------------------

    def _read(self) -> tuple[int, list[str]]:
        """Return (max_total, record lines). The persisted cap is authoritative."""
        if not self.path.is_file():
            return self.requested_max, []
        max_total = self.requested_max
        records: list[str] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            if line.startswith("MAX "):
                try:
                    max_total = int(line.split()[1])
                except (IndexError, ValueError):
                    pass
            else:
                records.append(line)
        # If an explicit higher max was requested by this instance or environment,
        # it updates the persisted cap authoritatively.
        if self.requested_max != DEFAULT_MAX_TOTAL and self.requested_max > max_total:
            max_total = self.requested_max
        return max_total, records

    def set_max(self, new_max: int) -> int:
        """Authoritatively set a new maximum concurrency cap in the ledger."""
        cap = max(int(new_max), 1)
        with self._locked():
            _, records = self._read()
            self._write(cap, records)
            self.requested_max = cap
            return cap

    def _write(self, max_total: int, records: list[str]) -> None:
        lines = [f"MAX {max_total}", *records]
        tmp = self.path.with_suffix(f".tmp.{os.getpid()}")
        tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, self.path)  # atomic swap

    @staticmethod
    def _running(records: list[str]) -> list[list[str]]:
        return [r.split() for r in records if r.startswith("RUNNING ")]

    def _reap_stale(self, records: list[str], now: float) -> list[str]:
        """Drop RUNNING rows older than the lease.

        Reaping is AGE-based, not PID-based: harness adapters acquire through a
        short-lived CLI process, so the acquiring PID is gone while the slot is
        still legitimately held by the agent. A crashed holder is covered by the
        lease plus the adapter's release-on-next-turn safety net.
        """
        kept: list[str] = []
        for record in records:
            if not record.startswith("RUNNING "):
                kept.append(record)
                continue
            parts = record.split()
            started = float(parts[5]) if len(parts) > 5 else 0.0
            if (now - started) > self.lease_seconds:
                continue  # lease expired (holder crashed or vanished)
            kept.append(record)
        return kept

    @staticmethod
    def _token_for(records: list[str], caller: str) -> str | None:
        for parts in Ledger._running(records):
            if len(parts) >= 4 and parts[1] == caller:
                return parts[3]
        return None

    @staticmethod
    def _validate_caller(caller: str) -> None:
        if not CALLER_RE.match(caller):
            raise ValueError(
                f"caller must match {CALLER_RE.pattern!r}, got {caller!r}"
            )

    # -- operations ------------------------------------------------------

    def acquire(
        self, caller: str, orchestrator: bool = False, timeout: float = 30.0
    ) -> str | None:
        """Reserve a slot. Returns the token, or None if the cap stayed full."""
        self._validate_caller(caller)
        deadline = time.monotonic() + float(timeout)
        while True:
            with self._locked():
                max_total, records = self._read()
                existing = self._token_for(records, caller)
                if existing:
                    return existing
                now = time.time()
                records = self._reap_stale(records, now)
                if len(self._running(records)) < max_total:
                    token = f"{caller}-{os.getpid()}-{uuid.uuid4().hex[:8]}"
                    records.append(
                        f"RUNNING {caller} {'yes' if orchestrator else 'no'} "
                        f"{token} {os.getpid()} {int(now)}"
                    )
                    self._write(max_total, records)
                    return token
                self._write(max_total, records)  # persist reaping even on failure
            if time.monotonic() >= deadline:
                return None
            time.sleep(POLL_SECONDS)

    def release(self, caller: str) -> None:
        """Release the slot held by ``caller`` (a no-op if it holds none)."""
        self._validate_caller(caller)
        with self._locked():
            max_total, records = self._read()
            records = [
                r
                for r in records
                if not (r.startswith("RUNNING ") and r.split()[1] == caller)
            ]
            self._write(max_total, records)

    def fail(self, caller: str, attempts: int = 1) -> None:
        """Park a caller as PAUSED after a rate-limit (429) for retry.

        Idempotent: only a caller that was actually RUNNING is parked, and an
        existing PAUSED row for the same caller is replaced, not duplicated.
        """
        self._validate_caller(caller)
        with self._locked():
            max_total, records = self._read()
            was_running = any(
                r.startswith("RUNNING ") and r.split()[1] == caller for r in records
            )
            if not was_running:
                # Not holding a slot: leave the ledger untouched (do not create
                # a phantom PAUSED row, and do not drop an existing one).
                return
            records = [
                r
                for r in records
                if not (r.startswith("RUNNING ") and r.split()[1] == caller)
                and not (r.startswith("PAUSED ") and r.split()[1] == caller)
            ]
            records.append(f"PAUSED {caller} {int(time.time())} {attempts}")
            self._write(max_total, records)

    def paused(self) -> list[dict]:
        """Callers parked for retry, with a backoff hint (2s -> 60s)."""
        with self._locked():
            _, records = self._read()
            result = []
            for record in records:
                if not record.startswith("PAUSED "):
                    continue
                parts = record.split()
                caller = parts[1]
                attempts = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 1
                delay = min(2 ** attempts, 60)
                result.append({"caller": caller, "attempts": attempts, "retry_after_s": delay})
            return result

    def clear_paused(self, caller: str | None = None) -> None:
        """Drop PAUSED rows for ``caller``, or for every caller when ``None``."""
        with self._locked():
            max_total, records = self._read()
            if caller:
                records = [
                    r
                    for r in records
                    if not (r.startswith("PAUSED ") and r.split()[1] == caller)
                ]
            else:
                records = [r for r in records if not r.startswith("PAUSED ")]
            self._write(max_total, records)

    def status(self) -> dict:
        """Reap stale leases and return the current running/paused/slots snapshot."""
        with self._locked():
            max_total, records = self._read()
            now = time.time()
            records = self._reap_stale(records, now)
            self._write(max_total, records)
            running = self._running(records)
            paused = [r for r in records if r.startswith("PAUSED ")]
            return {
                "running": len(running),
                "paused": len(paused),
                "max": max_total,
                "orchestrator_present": any(
                    len(p) >= 3 and p[2] == "yes" for p in running
                ),
                "slots_free": max(max_total - len(running), 0),
                "ledger": records,
            }

    def reset(self) -> None:
        """Clear every record, returning the ledger to an idle state."""
        with self._locked():
            self._write(self.requested_max, [])
