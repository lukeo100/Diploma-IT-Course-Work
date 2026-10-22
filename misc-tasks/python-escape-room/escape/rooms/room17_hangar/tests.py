from escape.testkit import expect, need_attr, need_class, need_method


def test_init(s):
    """Robot("R2") has a name, a full battery and position 0"""
    robot = need_class(s, "Robot")("R2")
    expect(need_attr(robot, "name"), "R2", 'Robot("R2").name')
    expect(need_attr(robot, "battery"), 100, 'Robot("R2").battery')
    expect(need_attr(robot, "position"), 0, 'Robot("R2").position')


def test_init_battery(s):
    """Robot can be given a starting battery"""
    robot = need_class(s, "Robot")("Bolt", 30)
    expect(need_attr(robot, "battery"), 30, 'Robot("Bolt", 30).battery')


def test_move(s):
    """move() moves the robot and uses battery"""
    robot = need_class(s, "Robot")("R2")
    expect(need_method(robot, "move")(3), True, "robot.move(3)", verb="should return")
    expect(robot.position, 3, "position after move(3)")
    expect(robot.battery, 70, "battery after move(3)")
    robot.move(2)
    expect(robot.position, 5, "position after move(3) then move(2)")


def test_move_not_enough_battery(s):
    """move() refuses when there isn't enough battery"""
    robot = need_class(s, "Robot")("R2", 25)
    expect(need_method(robot, "move")(3), False, 'Robot("R2", 25).move(3)', verb="should return")
    expect(robot.position, 0, "position after a move that failed")
    expect(robot.battery, 25, "battery after a move that failed")
    expect(robot.move(2), True, 'then move(2), with exactly enough battery,', verb="should return")
    expect(robot.battery, 5, "battery after move(2)")


def test_recharge(s):
    """recharge() adds battery, up to 100"""
    robot = need_class(s, "Robot")("R2", 20)
    need_method(robot, "recharge")(30)
    expect(robot.battery, 50, "battery after recharge(30) from 20")
    robot.recharge(80)
    expect(robot.battery, 100, "battery after recharge(80) from 50")


def test_status(s):
    """status() describes the robot"""
    robot = need_class(s, "Robot")("R2")
    robot.move(3)
    expect(need_method(robot, "status")(), "R2 is at 3 with 70% battery", "status() after move(3)",
           verb="should return")


def test_robots_are_separate(s):
    """Two robots keep their own battery and position"""
    Robot = need_class(s, "Robot")
    first, second = Robot("A"), Robot("B")
    first.move(4)
    expect(second.position, 0, "the second robot's position after the first one moved")
    expect(second.battery, 100, "the second robot's battery after the first one moved")
