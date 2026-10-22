"""Checks one student solution against its room's tests.

This runs in its own Python process (started by checker.py), so a crash or
an endless loop in student code can never freeze the game.

Usage: python runner.py <game_dir> <room_id> <solution_file>
Prints one line: MARKER followed by the result as JSON.
"""
import builtins
import importlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import traceback
import types
from pathlib import Path

MARKER = "@@ESCAPE-RESULT@@"
MAX_OUTPUT = 4000

EXIT_MESSAGE = (
    "Your code called exit() or quit(), which stops Python before the game "
    "can check it. Remove that line."
)


class InputNotAllowed(Exception):
    pass


def no_input(prompt=""):
    raise InputNotAllowed(
        "input() was called while the game was checking your code. The game "
        "can't type answers for you. Move input() into the "
        "`if __name__ == \"__main__\":` block at the bottom of your file."
    )


def error_info(exc, filename):
    """Describe an exception, pointing at the last line of the student's own file it went through."""
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == filename]
    last = frames[-1] if frames else None
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "line": last.lineno if last else None,
        "code": (last.line or "").strip() if last else None,
    }


def load_tests(game_dir, room_id):
    path = game_dir / "escape" / "rooms" / room_id / "tests.py"
    spec = importlib.util.spec_from_file_location("room_tests", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [
        ((func.__doc__ or name).strip(), func)
        for name, func in vars(module).items()
        if name.startswith("test_") and callable(func)
    ]


def run_test(name, test, student, filename, fail_class):
    try:
        test(student)
    except fail_class as exc:
        return {"name": name, "passed": False, "message": str(exc)}
    except SystemExit:
        return {"name": name, "passed": False, "message": EXIT_MESSAGE}
    except Exception as exc:
        info = error_info(exc, filename)
        where = " (line {} of your file)".format(info["line"]) if info["line"] else ""
        message = "Your code crashed with {}: {}{}".format(info["type"], info["message"], where)
        return {"name": name, "passed": False, "message": message, "error": info}
    return {"name": name, "passed": True}


def run(game_dir, room_id, solution, captured):
    filename = str(solution)
    try:
        source = solution.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"status": "error", "error": {
            "type": "UnicodeDecodeError", "line": None, "code": None,
            "message": "Your file isn't saved as UTF-8 text. Change the encoding to UTF-8 in your editor and save again.",
        }}

    try:
        code = compile(source, filename, "exec")
    except SyntaxError as exc:
        return {"status": "syntax_error", "error": {
            "type": type(exc).__name__,
            "message": exc.msg,
            "line": exc.lineno,
            "column": exc.offset,
            "code": (exc.text or "").rstrip("\r\n"),
        }}

    testkit = importlib.import_module("escape.testkit")
    testkit.ROOM_DIR = game_dir / "escape" / "rooms" / room_id
    testkit.SCRATCH = Path(tempfile.mkdtemp(prefix="escape-room-"))
    tests = load_tests(game_dir, room_id)

    student = types.ModuleType("student")
    student.__file__ = filename
    sys.modules["student"] = student
    builtins.input = no_input
    sys.stdout = captured
    try:
        exec(code, student.__dict__)
    except SystemExit:
        return {"status": "error", "error": {"type": "SystemExit", "message": EXIT_MESSAGE, "line": None, "code": None}}
    except Exception as exc:
        return {"status": "error", "error": error_info(exc, filename)}
    student.__escape_output__ = captured.getvalue()

    results = [run_test(name, test, student, filename, testkit.Fail) for name, test in tests]
    passed = all(r["passed"] for r in results)
    return {"status": "pass" if passed else "fail", "tests": results}


def main():
    game_dir, room_id, solution = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    sys.path.insert(0, str(game_dir))

    real_stdout = sys.stdout
    captured = io.StringIO()
    try:
        result = run(game_dir, room_id, solution, captured)
    finally:
        sys.stdout = real_stdout
        scratch = getattr(sys.modules.get("escape.testkit"), "SCRATCH", None)
        if scratch:
            shutil.rmtree(str(scratch), ignore_errors=True)

    output = captured.getvalue()
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + "\n... (output cut short)"
    result["output"] = output
    real_stdout.write(MARKER + json.dumps(result) + "\n")
    real_stdout.flush()


if __name__ == "__main__":
    main()
