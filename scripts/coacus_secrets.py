#!/usr/bin/env python3
"""Run the pinned, checksum-verified secret scanner using portable Python tooling."""

from __future__ import annotations

import argparse
import hashlib
import io
import platform
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# Publisher release and checksums resolved 2026-10-02:
# https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1
VERSION = "8.30.1"
CHECKSUMS = {
    ("darwin", "arm64"): "b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5",
    ("darwin", "x64"): "dfe101a4db2255fc85120ac7f3d25e4342c3c20cf749f2c20a18081af1952709",
    ("linux", "arm64"): "e4a487ee7ccd7d3a7f7ec08657610aa3606637dab924210b3aee62570fb4b080",
    ("linux", "x64"): "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb",
    ("windows", "arm64"): "b95f5e4f5c425cedca7ee203d9afd29597e692c4924a12ed42f970537c72cc0f",
    ("windows", "x64"): "d29144deff3a68aa93ced33dddf84b7fdc26070add4aa0f4513094c8332afc4e",
}


def install_binary(content: bytes, checksum: str, target: Path) -> None:
    """Reject checksum drift, then copy only the named regular executable."""
    if hashlib.sha256(content).hexdigest() != checksum:
        raise ValueError("gitleaks download checksum mismatch")
    buffer = io.BytesIO(content)
    if target.suffix == ".exe":
        with zipfile.ZipFile(buffer) as archive:
            binary = archive.read("gitleaks.exe")
    else:
        with tarfile.open(fileobj=buffer, mode="r:gz") as archive:
            member = archive.getmember("gitleaks")
            if not member.isfile():
                raise ValueError("gitleaks archive executable is not a regular file")
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError("gitleaks archive has no executable")
            with stream:
                binary = stream.read()
    target.write_bytes(binary)
    target.chmod(0o700)


def main(argv: list[str] | None = None) -> int:
    """Download the host's verified scanner and return its scan exit status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64"}.get(machine, machine)
    checksum = CHECKSUMS.get((system, arch))
    if checksum is None:
        parser.error(f"no pinned scanner binary for {system}/{arch}")
    extension = "zip" if system == "windows" else "tar.gz"
    url = f"https://github.com/gitleaks/gitleaks/releases/download/v{VERSION}/gitleaks_{VERSION}_{system}_{arch}.{extension}"
    with tempfile.TemporaryDirectory(prefix="coacus-secrets-") as tmp:
        target = Path(tmp) / ("gitleaks.exe" if system == "windows" else "gitleaks")
        # URL is the fixed HTTPS publisher release; archive integrity is pinned.
        with urllib.request.urlopen(url, timeout=60) as response:  # nosec B310
            install_binary(response.read(), checksum, target)
        # Scan the checked-out state that squash-merge ships; redact all matches.
        return subprocess.run(
            [str(target), "dir", "--redact", "--no-banner", "--exit-code", "1",
             "--config", str(args.root / ".gitleaks.toml"), str(args.root)],
            check=False,
        ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
