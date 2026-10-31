#!/usr/bin/env python3
"""Run matching tests sequentially to identify newly created state.

Usage: find_polluter.py <path-to-check> <test-glob> [-- <runner> ...]
Default adapter: npm test <matched-file>. Select the project's actual runner.
Exit 0: executed cases clean; 1: polluter found; 2: inconclusive/usage error.
This is a sequential search, not bisection; no files or contents are removed/read.
"""
from __future__ import annotations

import glob
from pathlib import Path
import subprocess
import sys


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if len(args) < 2 or (len(args) > 2 and (args[2] != '--' or len(args) < 4)):
        print('Usage: find_polluter.py <path-to-check> <test-glob> [-- <runner> ...]')
        return 2
    target, pattern = Path(args[0]), args[1]
    runner = args[3:] if len(args) > 2 else ['npm', 'test']
    tests = sorted({Path(item) for item in glob.glob(pattern, recursive=True) if Path(item).is_file()})
    executed = failed = 0

    def report(status: str, code: int) -> int:
        print(f'Result: {status}; matched={len(tests)} executed={executed} failed={failed} skipped={len(tests)-executed}')
        return code

    if target.exists() or target.is_symlink():
        return report('inconclusive (pollution already exists)', 2)
    if not tests:
        return report('inconclusive (no matching tests)', 2)
    for test in tests:
        executed += 1
        try:
            result = subprocess.run([*runner, str(test)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            failed += 1
            return report('inconclusive (runner unavailable)', 2)
        if result.returncode:
            failed += 1
            return report('inconclusive (runner failed; inspect the case separately)', 2)
        if target.exists() or target.is_symlink():
            print(f'FOUND POLLUTER: {test}; created path: {target}')
            # Metadata only; never print the created content, which may be a credential.
            print(f'Created entry size: {target.lstat().st_size} bytes')
            return report('polluter found', 1)
    return report('executed cases clean (limited to this pattern and runner)', 0)


if __name__ == '__main__':
    raise SystemExit(main())
