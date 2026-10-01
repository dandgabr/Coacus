#!/usr/bin/env python3
"""Bisection script to find which test creates unwanted files/state.

Usage: python3 find_polluter.py <file_or_dir_to_check> <test_pattern>
Example: python3 find_polluter.py '.git' 'src/**/*.test.ts'
"""

from __future__ import annotations

import glob
import os
import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 2:
        print("Usage: find_polluter.py <file_to_check> <test_pattern>")
        print("Example: find_polluter.py '.git' 'src/**/*.test.ts'")
        return 1

    pollution_check = args[0]
    test_pattern = args[1]
    if test_pattern.startswith("./"):
        test_pattern = test_pattern[2:]

    print(f"🔍 Searching for test that creates: {pollution_check}")
    print(f"Test pattern: {test_pattern}\n")

    # Match recursively
    matched_files = set(glob.glob(f"./{test_pattern}", recursive=True))
    collapsed = test_pattern.replace("**/", "")
    matched_files.update(glob.glob(f"./{collapsed}", recursive=True))

    test_files = sorted(f for f in matched_files if os.path.isfile(f))
    total = len(test_files)
    print(f"Found {total} test files\n")

    for count, test_file in enumerate(test_files, 1):
        if os.path.exists(pollution_check):
            print(f"⚠️  Pollution already exists before test {count}/{total}")
            print(f"   Skipping: {test_file}")
            continue

        print(f"[{count}/{total}] Testing: {test_file}")

        # Run npm test (or framework equivalent)
        subprocess.run(["npm", "test", test_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(pollution_check):
            print("\n🎯 FOUND POLLUTER!")
            print(f"   Test: {test_file}")
            print(f"   Created: {pollution_check}\n")
            print("Pollution details:")
            subprocess.run(["ls", "-la", pollution_check])
            print("\nTo investigate:")
            print(f"  npm test {test_file}    # Run just this test")
            print(f"  cat {test_file}         # Review test code")
            return 1

    print("\n✅ No polluter found - all tests clean!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
