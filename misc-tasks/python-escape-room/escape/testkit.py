"""Helpers for each room's tests.py.

A test is a function named test_... that takes the student's module. Its
docstring is the check's name on the game page. A test fails by raising
Fail with a message written for the student.
"""
import ast
import copy
import shutil
import traceback
from pathlib import Path

# Set by runner.py before the tests load.
ROOM_DIR = None  # this room's folder in escape/rooms/
SCRATCH = None   # a temporary folder, deleted after the check


class Fail(Exception):
    """A check didn't pass. The message is shown to the student."""


TYPE_WORDS = {
    str: "a str (text in quotes)",
    int: "an int (a whole number, no quotes)",
    float: "a float (a number with a decimal point)",
    bool: "a bool (True or False, no quotes)",
    list: "a list",
    tuple: "a tuple",
    dict: "a dict",
    type(None): "None",
}

RETURN_TIP = "Did you forget to `return` the answer?"
VARIABLE_TIP = "Replace the None with your answer."


def type_word(kind):
    return TYPE_WORDS.get(kind, "a " + kind.__name__)


def need_variable(student, name):
    if not hasattr(student, name):
        raise Fail("I can't find a variable called `{}` in your file. Check the spelling.".format(name))
    return getattr(student, name)


def need_function(student, name):
    func = getattr(student, name, None)
    if func is None:
        raise Fail(
            "I can't find a function called `{0}` in your file. "
            "Check the spelling, and that it starts with `def {0}(`.".format(name)
        )
    if not callable(func):
        raise Fail("`{}` should be a function, but it is {}.".format(name, type_word(type(func))))
    return func


def expect_type(value, wanted, what):
    if type(value) is wanted:
        return
    message = "`{}` should be {}, but it is {!r}".format(what, type_word(wanted), value)
    if value is None:
        message += ". " + VARIABLE_TIP
    else:
        message += ", which is {}.".format(type_word(type(value)))
    raise Fail(message)


def expect(got, expected, what, verb="should be", none_tip=VARIABLE_TIP):
    # Types must match too, so 3.0 doesn't pass for 3 and [2, 5] doesn't pass for (2, 5).
    if got == expected and type(got) is type(expected):
        return
    if got == expected:
        message = "`{}` {} {!r}, which is {}, but it was {!r}, which is {}.".format(
            what, verb, expected, type_word(type(expected)), got, type_word(type(got)))
    else:
        message = "`{}` {} {!r}, but it was {!r}.".format(what, verb, expected, got)
        if got is None and none_tip:
            message += " " + none_tip
    raise Fail(message)


def show_call(name, args, kwargs):
    parts = [repr(a) for a in args] + ["{}={!r}".format(k, v) for k, v in kwargs.items()]
    return "{}({})".format(name, ", ".join(parts))


def check_call(student, name, args, expected, kwargs=None):
    """Call student.name(*args, **kwargs) and check that it returns expected."""
    func = need_function(student, name)
    if not isinstance(args, tuple):
        args = (args,)
    kwargs = kwargs or {}
    # Copies, so a student function that changes its arguments can't affect later checks.
    got = func(*copy.deepcopy(args), **copy.deepcopy(kwargs))
    expect(got, expected, show_call(name, args, kwargs), verb="should return", none_tip=RETURN_TIP)


def printed(student):
    """Everything the student's file printed while it loaded."""
    return getattr(student, "__escape_output__", "")


def expect_raises(action, exc_type, what):
    """Check that calling action() raises exc_type."""
    try:
        got = action()
    except exc_type:
        return
    except Exception as exc:
        raise Fail("`{}` should raise {}, but it raised {}: {}".format(
            what, exc_type.__name__, type(exc).__name__, exc))
    raise Fail("`{}` should raise {}, but it returned {!r} instead.".format(what, exc_type.__name__, got))


def check_raises(student, name, args, exc_type, kwargs=None):
    """Call student.name(*args, **kwargs) and check that it raises exc_type."""
    func = need_function(student, name)
    if not isinstance(args, tuple):
        args = (args,)
    kwargs = kwargs or {}
    expect_raises(lambda: func(*copy.deepcopy(args), **copy.deepcopy(kwargs)),
                  exc_type, show_call(name, args, kwargs))


# ----- classes ------------------------------------------------------------

def need_class(student, name):
    cls = getattr(student, name, None)
    if cls is None:
        raise Fail(
            "I can't find a class called `{0}` in your file. "
            "Check the spelling, and that it starts with `class {0}`.".format(name))
    if not isinstance(cls, type):
        raise Fail("`{}` should be a class, but it is {}.".format(name, type_word(type(cls))))
    return cls


def need_attr(obj, name, where="__init__"):
    """Get obj.name, failing with a helpful message if it's missing."""
    if not hasattr(obj, name):
        raise Fail("{} objects need a `{}` attribute. Set `self.{}` in {}.".format(
            type(obj).__name__, name, name, where))
    return getattr(obj, name)


def need_method(obj, name):
    method = getattr(obj, name, None)
    if not callable(method):
        raise Fail("{} objects need a `{}()` method. Add `def {}(self, ...):` inside the class.".format(
            type(obj).__name__, name, name))
    return method


# ----- files ----------------------------------------------------------------

def data_file(name):
    """A fresh copy of one of this room's data files, in a temporary folder,
    so a student editing their own copy can't break the checks."""
    target = SCRATCH / name
    shutil.copyfile(str(ROOM_DIR / "files" / name), str(target))
    return str(target)


def write_file(name, text):
    """Make a temporary file for a check and return its path."""
    target = SCRATCH / name
    target.write_text(text, encoding="utf-8")
    return str(target)


def scratch_path(name):
    """A path in the temporary folder for the student's code to write to."""
    return str(SCRATCH / name)


# ----- looking at how the code is written ------------------------------------

def find_function(student, name):
    tree = ast.parse(Path(student.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    raise Fail("I can't find a function called `{0}` in your file. It should start with `def {0}(`.".format(name))


def need_recursion(student, name):
    node = find_function(student, name)
    calls_itself = any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name
        for n in ast.walk(node))
    if not calls_itself:
        raise Fail("`{0}` gives the right answers but doesn't call itself. "
                   "This room needs recursion: `{0}` must call `{0}(...)`.".format(name))


def need_comprehension(student, name):
    node = find_function(student, name)
    found = any(isinstance(n, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)) for n in ast.walk(node))
    loops = any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(node))
    if not found or loops:
        raise Fail("`{}` gives the right answers, but this room needs a comprehension "
                   "instead of a for loop, like `[x for x in items if ...]`.".format(name))


# ----- running the student's own tests ---------------------------------------

def try_call(func, *args):
    """Call func and return the exception it raised, or None."""
    try:
        func(*args)
    except Exception as exc:
        return exc
    return None


def explain(exc, student):
    """Short description of an exception, with the line in the student's file."""
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == student.__file__]
    where = " on line {}".format(frames[-1].lineno) if frames else ""
    text = "{}{}".format(type(exc).__name__, where)
    if frames and frames[-1].line:
        text += ": `{}`".format(frames[-1].line.strip())
    elif str(exc):
        text += ": {}".format(exc)
    return text
