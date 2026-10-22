from escape.testkit import expect, expect_raises, need_attr, need_class, need_method


def new_locker(s):
    return need_class(s, "Locker")("Sam", 1234)


def open_locker(s, coins=0):
    locker = new_locker(s)
    need_method(locker, "unlock")(1234)
    if coins:
        need_method(locker, "deposit")(coins)
    return locker


def test_init(s):
    """A new locker is locked and empty"""
    locker = new_locker(s)
    expect(need_attr(locker, "owner"), "Sam", "locker.owner")
    expect(need_attr(locker, "coins"), 0, "locker.coins")
    expect(need_attr(locker, "locked"), True, "locker.locked")


def test_unlock(s):
    """unlock() only opens with the right pin"""
    locker = new_locker(s)
    expect(need_method(locker, "unlock")(1111), False, "unlock(1111) with the wrong pin", verb="should return")
    expect(locker.locked, True, "locked after a wrong pin")
    expect(locker.unlock(1234), True, "unlock(1234)", verb="should return")
    expect(locker.locked, False, "locked after the right pin")


def test_lock(s):
    """lock() locks it again"""
    locker = open_locker(s)
    need_method(locker, "lock")()
    expect(locker.locked, True, "locked after lock()")


def test_locked_refuses(s):
    """A locked locker refuses deposits and withdrawals"""
    locker = new_locker(s)
    expect(need_method(locker, "deposit")(10), False, "deposit(10) while locked", verb="should return")
    expect(locker.coins, 0, "coins after a refused deposit")
    expect(need_method(locker, "withdraw")(10), False, "withdraw(10) while locked", verb="should return")


def test_deposit_withdraw(s):
    """deposit() and withdraw() move coins when unlocked"""
    locker = open_locker(s)
    expect(need_method(locker, "deposit")(50), True, "deposit(50)", verb="should return")
    expect(locker.coins, 50, "coins after deposit(50)")
    expect(need_method(locker, "withdraw")(20), True, "withdraw(20)", verb="should return")
    expect(locker.coins, 30, "coins after withdraw(20)")
    expect(locker.withdraw(30), True, "withdraw(30), taking every coin,", verb="should return")
    expect(locker.coins, 0, "coins after taking every coin")


def test_bad_deposits(s):
    """deposit() raises ValueError for 0 or negative amounts"""
    locker = open_locker(s)
    deposit = need_method(locker, "deposit")
    expect_raises(lambda: deposit(0), ValueError, "deposit(0)")
    expect_raises(lambda: deposit(-5), ValueError, "deposit(-5)")
    expect(locker.coins, 0, "coins after refused deposits")


def test_bad_withdrawals(s):
    """withdraw() raises ValueError for bad amounts"""
    locker = open_locker(s, coins=10)
    withdraw = need_method(locker, "withdraw")
    expect_raises(lambda: withdraw(11), ValueError, "withdraw(11) with only 10 coins")
    expect_raises(lambda: withdraw(0), ValueError, "withdraw(0)")
    expect(locker.coins, 10, "coins after refused withdrawals")
