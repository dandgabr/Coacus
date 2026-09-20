#!/usr/bin/env python3
"""Behavior-eval runner for Coacus (testing).

Deterministic by default; live evaluation is opt-in.

    # static validation only (safe for CI, no LLM, no network)
    python3 scripts/coacus_eval.py validate

    # live run against a harness CLI installed locally
    python3 scripts/coacus_eval.py run [--scenario <id>] [--harness codex]
        [--judge-cmd "<command that reads the transcript on stdin>"]
        [--judge-agent]            # delegate judgment to a subagent via the harness

Live scenarios drive a real agent CLI, so they need the CLI + credentials and
run outside CI. Each harness declares its non-interactive invocation in
`harnesses/<h>/harness.json` (`live_cli`); a harness without one is reported as
`NO_RUNNER`. `--harness` overrides the scenario's target so one scenario can be
exercised against any locally installed live CLI. Deterministic checks
(`contains`/`not_contains`/`regex`) run on the captured transcript; the `rubric`
is passed to the judge.

The `--judge-cmd` receives JSON on stdin: {"scenario": {...}, "transcript": "..."}
and must print a verdict line (anything). `--judge-agent` runs the rubric through
the same harness as an orchestrated subagent (multi-agent-orchestrator pattern).
"""

from __future__ import annotations

import argparse
import os
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.validators import evals as scenario_validator  # noqa: E402

# Live CLI per harness is DATA: each harness.json may declare a `live_cli`
# invocation (e.g. ["opencode", "run"], ["codex", "exec"], ["agy", "--print"]).
# A harness without one cannot run live and is reported as NO_RUNNER. The
# constant is the fallback for a minimal repo whose manifests declare none.
HARNESS_CLI = {"opencode": ["opencode", "run"]}
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _live_clis(root: Path) -> dict[str, list[str]]:
    """Map harness name -> live CLI argv prefix, read from harness.json."""
    clis: dict[str, list[str]] = {}
    harnesses_dir = root / "harnesses"
    if harnesses_dir.is_dir():
        for manifest in sorted(harnesses_dir.glob("*/harness.json")):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            name = data.get("name")
            cli = data.get("live_cli")
            if isinstance(name, str) and isinstance(cli, list) and all(
                isinstance(part, str) and part for part in cli
            ):
                clis[name] = cli
    return clis or dict(HARNESS_CLI)


def _redact(text: str) -> str:
    """Redact a live transcript/verdict for logs.

    An agent transcript may contain whatever the model saw (including any
    credentials present in the environment), so we do not echo it by default.
    Set COACUS_EVAL_VERBOSE=1 to print a bounded excerpt for local debugging.
    """
    if os.environ.get("COACUS_EVAL_VERBOSE") == "1":
        return text[:400]
    return f"<redacted {len(text)} chars; set COACUS_EVAL_VERBOSE=1 to print>"


def _scenarios(root: Path) -> dict[str, dict]:
    """Load scenarios; malformed ones are reported, not fatal."""
    out: dict[str, dict] = {}
    for path in scenario_validator.discover(root):
        try:
            out[path.parent.name] = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise SystemExit(f"{path}: unreadable scenario ({exc})")
    return out


def _apply_checks(scenario: dict, transcript: str) -> list[dict]:
    results: list[dict] = []
    for check in scenario.get("checks", []):
        kind = check["kind"]
        value = str(check["value"])
        if kind == "contains":
            ok = value in transcript
        elif kind == "not_contains":
            ok = value not in transcript
        else:  # regex
            ok = re.search(value, transcript) is not None
        results.append({"kind": kind, "value": value, "passed": ok})
    return results


def _run_harness(scenario: dict, timeout: float, clis: dict[str, list[str]]) -> tuple[str, str]:
    """Run the harness CLI. Returns (cleaned transcript, status)."""
    harness = scenario["harness"]
    cli = clis.get(harness)
    if not cli:
        return "", f"NO_RUNNER ({harness})"
    try:
        proc = subprocess.run(
            [*cli, scenario["prompt"]],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return "", f"NO_CLI ({cli[0]})"
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT"
    if proc.returncode != 0:
        return "", f"EXIT_{proc.returncode}"
    stdout = ANSI.sub("", proc.stdout).strip()
    stderr = ANSI.sub("", proc.stderr).strip()
    # Most harnesses print the answer on stdout and their banner on stderr, so
    # prefer stdout; fall back to stderr when stdout is empty (some CLIs and
    # wrappers emit the reply there), rather than reporting an empty transcript.
    combined = stdout or stderr
    return combined, "OK"


def _judge(scenario: dict, transcript: str, judge_cmd: str | None, judge_agent: bool,
           clis: dict[str, list[str]]) -> dict:
    payload = json.dumps({"scenario": scenario, "transcript": transcript})
    if judge_agent:
        # Route the rubric through the harness as an orchestrated subagent.
        cli = clis.get(scenario["harness"]) or clis.get("opencode") or ["opencode", "run"]
        prompt = (
            "You are a strict verifier. Given this JSON with a scenario and a "
            "transcript, judge whether the transcript satisfies each rubric item. "
            "Reply with exactly one line: 'VERDICT: PASS' or 'VERDICT: FAIL', "
            "followed by one line per rubric item.\n\n" + payload
        )
        try:
            proc = subprocess.run(
                [*cli, prompt], cwd=ROOT, capture_output=True, text=True, timeout=600
            )
            out = ANSI.sub("", proc.stdout).strip()
            return {"mode": "agent", "verdict": out, "passed": _verdict_pass(out)}
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            return {"mode": "agent", "verdict": f"unavailable ({exc})", "passed": None}
    if judge_cmd:
        try:
            proc = subprocess.run(
                shlex.split(judge_cmd),
                input=payload,
                capture_output=True,
                text=True,
                timeout=600,
            )
            out = (proc.stdout or proc.stderr).strip()
            return {"mode": "cmd", "verdict": out, "passed": _verdict_pass(out)}
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            return {"mode": "cmd", "verdict": f"unavailable ({exc})", "passed": None}
    return {"mode": "deterministic", "verdict": "checks only (no judge configured)", "passed": None}


def _verdict_pass(text: str) -> bool | None:
    """A judge verdict gates pass/fail only when it is explicit."""
    match = re.search(r"(?i)VERDICT:\s*(PASS|FAIL)", text)
    if match:
        return match.group(1).upper() == "PASS"
    return None  # unknown verdict is advisory, does not gate


def cmd_validate(root: Path) -> int:
    """Statically validate every eval scenario; return non-zero on any error."""
    errors = scenario_validator.validate(root)
    if errors:
        print(f"{len(errors)} scenario error(s):")
        for error in errors:
            print(f"  [error] {error}")
        return 1
    print("eval scenarios OK")
    return 0


def cmd_run(root: Path, scenario_id: str | None, judge_cmd: str | None, judge_agent: bool,
            timeout: float, harness: str | None = None) -> int:
    """Run scenarios live and report check/judge results; fail if any did not pass."""
    # Fail fast on invalid scenarios (same contract as the static gate).
    errors = scenario_validator.validate(root)
    if errors:
        print("cannot run: scenario validation failed")
        for error in errors:
            print(f"  [error] {error}")
        return 1
    scenarios = _scenarios(root)
    if not scenarios:
        print("no scenarios found")
        return 1
    if scenario_id and scenario_id not in scenarios:
        print(f"unknown scenario: {scenario_id}")
        return 1
    clis = _live_clis(root)
    if harness and harness not in clis:
        print(f"unknown harness: {harness} (no live_cli; available: {', '.join(sorted(clis))})")
        return 1
    selected = {scenario_id: scenarios[scenario_id]} if scenario_id else scenarios

    all_passed = True
    for sid, scenario in selected.items():
        if harness:
            # Override the scenario's harness so one scenario can be exercised
            # against any locally installed live CLI.
            scenario = {**scenario, "harness": harness}
        transcript, status = _run_harness(scenario, timeout, clis)
        checks = _apply_checks(scenario, transcript)
        judge = _judge(scenario, transcript, judge_cmd, judge_agent, clis)
        passed = status == "OK" and all(c["passed"] for c in checks)
        if judge.get("passed") is not None:
            passed = passed and judge["passed"]
        all_passed = all_passed and passed
        print(json.dumps({
            "scenario": sid,
            "harness": scenario["harness"],
            "status": status,
            "passed": passed,
            "checks": checks,
            "judge": {**judge, "verdict": _redact(str(judge.get("verdict", "")))},
            "transcript_excerpt": _redact(transcript),
        }, indent=2))
    return 0 if all_passed else 1


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to ``validate`` or ``run``."""
    parser = argparse.ArgumentParser(prog="coacus-eval", description=__doc__)
    parser.add_argument("action", choices=["validate", "run"])
    parser.add_argument("--scenario", help="run only this scenario id")
    parser.add_argument(
        "--harness",
        help="override the scenario's harness with a locally installed live CLI",
    )
    parser.add_argument("--judge-cmd", help="command reading the transcript JSON on stdin")
    parser.add_argument("--judge-agent", action="store_true", help="judge via an orchestrated subagent")
    parser.add_argument("--timeout", type=float, default=300.0)
    args = parser.parse_args(argv)
    if args.action == "validate":
        return cmd_validate(ROOT)
    return cmd_run(
        ROOT, args.scenario, args.judge_cmd, args.judge_agent, args.timeout, args.harness
    )


if __name__ == "__main__":
    raise SystemExit(main())
