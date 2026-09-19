"""On-disk concurrency governor with an flock-guarded slot ledger (D6/ADR-0007).

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
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

DEFAULT_MAX_TOTAL = 5
POLL_SECONDS = 0.2
DEFAULT_LEASE_SECONDS = 900
CALLER_RE = re.compile(r"^[A-Za-z0-9._:-]+$")


def state_dir() -> Path:
    override = os.environ.get("GOVERNOR_STATE_DIR")
    if override:
        return Path(override)
    runtime = os.environ.get("XDG_RUNTIME_DIR") or "/tmp"
    return Path(runtime) / "coacus-governor"


def _env_max_total() -> int:
    raw = os.environ.get("ORCH_MAX_CONCURRENT", str(DEFAULT_MAX_TOTAL))
    try:
        return max(int(raw), 1)
    except ValueError:
        return DEFAULT_MAX_TOTAL


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
    ):
        self.dir = Path(directory) if directory else state_dir()
        self.requested_max = int(max_total) if max_total is not None else _env_max_total()
        self.lease_seconds = int(lease_seconds) if lease_seconds else _lease_seconds()
        self.path = self.dir / "ledger"
        self.lock_path = self.dir / "ledger.lock"
        self.dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.dir, 0o700)
        self.lock_path.touch(exist_ok=True)

    # -- locking ---------------------------------------------------------

    @contextmanager
    def _locked(self):
        import fcntl  # POSIX; imported lazily so the module loads on Windows

        fd = os.open(self.lock_path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
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
        # A caller may never RAISE the cap; a lower request still governs.
        max_total = min(max_total, self.requested_max)
        return max_total, records

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
        with self._locked():
            self._write(self.requested_max, [])
