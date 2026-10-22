from escape.testkit import Fail, check_call, need_function


def test_average(s):
    """average counts every score"""
    check_call(s, "average", ([10, 20, 30],), 20.0)
    check_call(s, "average", ([7],), 7.0)
    check_call(s, "average", ([1, 2, 3, 4],), 2.5)


def test_all_doors_locked_true(s):
    """all_doors_locked is True when every door is locked"""
    check_call(s, "all_doors_locked", (["locked", "locked", "locked"],), True)
    check_call(s, "all_doors_locked", ([],), True)


def test_all_doors_locked_false(s):
    """all_doors_locked spots an open door anywhere in the list"""
    check_call(s, "all_doors_locked", (["open", "locked"],), False)
    check_call(s, "all_doors_locked", (["locked", "open"],), False)
    check_call(s, "all_doors_locked", (["locked", "locked", "open"],), False)


def test_add_tool_given_box(s):
    """add_tool adds to a toolbox it is given"""
    check_call(s, "add_tool", ("glue", ["tape"]), ["tape", "glue"])


def test_add_tool_new_box(s):
    """add_tool starts a new toolbox every time"""
    add_tool = need_function(s, "add_tool")
    first = add_tool("hammer")
    second = add_tool("saw")
    if first is second or second != ["saw"]:
        raise Fail(
            "Calling `add_tool(\"hammer\")` then `add_tool(\"saw\")` gave {!r} the second time, but it "
            "should be ['saw']. Both calls are sharing the same default list!".format(second))


def test_is_weekend(s):
    """is_weekend knows weekend days from weekdays"""
    check_call(s, "is_weekend", "Saturday", True)
    check_call(s, "is_weekend", "Sunday", True)
    check_call(s, "is_weekend", "Monday", False)
    check_call(s, "is_weekend", "Friday", False)
