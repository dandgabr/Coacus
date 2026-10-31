"""Probe Command Code tool-hook failure behavior with an isolated fake model.

Run only where the Command Code CLI is already available. This opt-in probe
uses a temporary home, a loopback server and a synthetic credential. The fake
model emits only a read_file call; it never requests a subagent. No provider
or user credential store is read. Network package installation is out of scope.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ALLOWED_EVENTS = {"tool_hook_blocked", "tool_completed", "tool_running", "mod_error"}


def selected_events(frames: list[object]) -> list[str]:
    """Keep only the fixed, non-sensitive event names used by this probe."""
    return sorted({x["event"].get("type") for x in frames
                   if isinstance(x, dict) and isinstance(x.get("event"), dict)
                   and isinstance(x["event"].get("type"), str)
                   and x["event"].get("type") in ALLOWED_EVENTS})


def main() -> int:
    """Run block and exception scenarios; return nonzero if either is unproved."""
    synthetic = ["synthetic-token-123", "person@example.test", "00000000-0000-0000-0000-000000000000"]
    if selected_events([{"event": {"type": value}} for value in synthetic]):
        return 1
    with tempfile.TemporaryDirectory(prefix="coacus-command-mod-probe-") as tmp:
        root = Path(tmp)
        home = root / "home"
        config = home / ".commandcode"
        config.mkdir(parents=True)
        (root / "sample.txt").write_text("synthetic-content\n", encoding="utf-8")
        state: dict[str, object] = {"requests": 0, "tools": []}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: object) -> None:
                pass

            def do_POST(self) -> None:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
                state["requests"] = int(state["requests"]) + 1
                state["tools"] = list(set(state["tools"]) | {
                    x.get("function", {}).get("name", "") for x in body.get("tools", [])})
                if state["requests"] == 1:
                    delta = {"role": "assistant", "tool_calls": [{"index": 0, "id": "probe-call-1",
                             "type": "function", "function": {"name": "read_file",
                             "arguments": json.dumps({"file_path": str(root / "sample.txt")})}}]}
                    finish = "tool_calls"
                else:
                    delta, finish = {"content": "probe completed"}, "stop"
                chunks = [
                    {"id": "probe-response", "object": "chat.completion.chunk", "created": 1,
                     "model": "probe-model", "choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
                    {"id": "probe-response", "object": "chat.completion.chunk", "created": 1,
                     "model": "probe-model", "choices": [{"index": 0, "delta": {}, "finish_reason": finish}]},
                ]
                raw = ("".join("data: " + json.dumps(x) + "\n\n" for x in chunks) + "data: [DONE]\n\n").encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        port = server.server_address[1]
        (config / "providers.json").write_text(json.dumps({"provider": {"probe": {
            "baseURL": f"http://127.0.0.1:{port}/v1", "apiKey": False,
            "models": {"probe-model": {"contextWindow": 32768}}}}}), encoding="utf-8")
        env = {key: os.environ[key] for key in ("PATH", "SYSTEMROOT", "WINDIR") if key in os.environ}
        env.update(HOME=str(home), USERPROFILE=str(home), TMPDIR=str(root), TEMP=str(root), TMP=str(root),
                   CMD_LOCAL_ONLY="1", DO_NOT_TRACK="1", COMMAND_CODE_API_KEY="synthetic-probe-key")
        failed = False
        try:
            for variant in ("block", "throw"):
                state.update(requests=0, tools=[])
                mark = root / (variant + ".seen")
                mod = root / (variant + ".ts")
                action = ("return {block:true, additionalContext:'PROBE_DENIED'};" if variant == "block"
                          else "throw new Error('synthetic-hook-failure');")
                mod.write_text("import {writeFileSync} from 'node:fs';\n"
                               "export default function(cmd) {cmd.hooks({beforeToolCall: ({toolName}) => {"
                               "writeFileSync(" + json.dumps(str(mark)) + ", toolName); " + action + "}});}\n", encoding="utf-8")
                command = ["command-code", "-p", "Execute the supplied synthetic probe.", "--local-only",
                           "--no-session", "--trust", "--skip-onboarding", "--max-turns", "3",
                           "--model", "probe/probe-model", "--output-format", "json", "--mod", str(mod)]
                try:
                    result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=50)
                except (OSError, subprocess.TimeoutExpired):
                    print(json.dumps({"variant": variant, "status": "unavailable"}))
                    failed = True
                    continue
                frames: list[object] = []
                for line in result.stdout.splitlines():
                    try:
                        frames.append(json.loads(line))
                    except ValueError:
                        pass
                events = selected_events(frames)
                expected = ("tool_hook_blocked" in events and "tool_running" not in events if variant == "block"
                            else {"mod_error", "tool_running", "tool_completed"}.issubset(events))
                called_read = mark.is_file() and mark.read_text(encoding="utf-8") == "read_file"
                passed = (result.returncode == 0 and int(state["requests"]) > 0
                          and "read_file" in state["tools"] and called_read and expected)
                failed |= not passed
                print(json.dumps({"variant": variant, "passed": passed, "events": events}))
        finally:
            server.shutdown()
            server.server_close()
        return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
