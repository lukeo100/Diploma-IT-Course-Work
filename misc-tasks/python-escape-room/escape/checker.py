"""Runs a room's tests against a solution file in a separate Python process."""
import json
import subprocess
import sys
from pathlib import Path

from .runner import MARKER

RUNNER = Path(__file__).resolve().with_name("runner.py")
TIME_LIMIT = 5


def check(game_dir, room_id, solution_path, time_limit=TIME_LIMIT):
    solution_path = Path(solution_path)
    if not solution_path.is_file():
        return {"status": "no_file"}

    # -I: ignore the student's environment, -B: don't write .pyc files,
    # -X utf8: same text encoding on every operating system.
    command = [sys.executable, "-I", "-B", "-X", "utf8", str(RUNNER),
               str(game_dir), room_id, str(solution_path)]
    try:
        proc = subprocess.run(
            command,
            cwd=str(solution_path.parent),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=time_limit,
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "limit": time_limit}

    for line in reversed(proc.stdout.splitlines()):
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER):])
    return {"status": "crash", "details": proc.stderr[-2000:]}
