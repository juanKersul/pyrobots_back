from routers.robot.robot_class import Robot,polar_to_rect,block_direction,calc_velocity

def test_polartorect1():
    res = polar_to_rect(270, 100, (0, 0))
    assert res == (0, 0)


def test_polartorect2():
    res = polar_to_rect(180 + 45, 999, (200, 400))
    assert res == (0, 200)


def test_polartorect3():
    res = polar_to_rect(179, 200, (100, 500))
    assert res == (0, 501)


def test_polartorect4():
    res = polar_to_rect(30, 999, (100, 500))
    assert res == (963, 999)


def test_blockdrirection1():
    res = block_direction(90, 50, 270)
    assert res == 270


def test_blockdrirection2():
    res = block_direction(90, 51, 270)
    assert res == 180


def test_blockdrirection3():
    res = block_direction(90, 40, 360)
    assert res == 0


def test_blockdrirection4():
    res = block_direction(220, 60, 270)
    assert res == 270


def test_calc_velocity1():
    res = calc_velocity(100, 0)
    assert res == 50


def test_calc_velocity2():
    res = calc_velocity(0, 100)
    assert res == 50


def test_calc_velocity3():
    res = calc_velocity(1000, 0)
    assert res == 50


def test_calc_velocity4():
    res = calc_velocity(80, 0)
    assert res == 40


def test_calc_velocity5():
    res = calc_velocity(0, 80)
    assert res == 30


def test_move1():
    robot1 = Robot((0, 0), 100)
    robot1.current_velocity = 0
    robot1.current_damage = 0
    robot1.drive(90, 100)
    robot1._move()
    assert robot1.current_position == (0, 100)
