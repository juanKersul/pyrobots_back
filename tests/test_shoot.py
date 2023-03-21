from routers.robot.robot_class import *
import random


def test_shoot_in_table():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.cannon_ammo = 1
    obj1.cannon_shoot = True
    obj1.current_damage = 100
    obj1.current_velocity = 100
    obj1.cannon(45, 200)
    obj1._shoot()
    assert obj1.misil_position[0] > -1 and obj1.misil_position[0] < 1000 and obj1.misil_position[1] > -1 and obj1.misil_position[1] < 1000



def test_shoot_false():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    obj1._shoot()
    assert obj1.misil_position == (None,None)


def test_random_in_range_1():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T2")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_2():
    obj1 = Robot(
        position=(950, 980),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T2")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_3():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.cannon_ammo = 1
    obj1.cannon_shoot = True
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T3")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_4():
    obj1 = Robot(
        position=(950, 980),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T4")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_5():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T5")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_6():
    obj1 = Robot(
        position=(950, 980),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T6")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_7():
    obj1 = Robot(
        position=(5, 990),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T7")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_8():
    obj1 = Robot(
        position=(990, 5),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T8")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_9():
    obj1 = Robot(
        position=(5, 990),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T9")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_10():
    obj1 = Robot(
        position=(990, 5),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T10")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_11():
    obj1 = Robot(
        position=(5, 990),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T11")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_in_range_12():
    obj1 = Robot(
        position=(990, 5),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    tup_test = (random.randint(0, 360), random.randint(0, 700))
    obj1.cannon(tup_test[0], tup_test[1])
    print("T12")
    print("Position -> ", obj1.current_position)
    print("(grados, distancia) ->", tup_test)
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_out_of_range_1():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    obj1.cannon(random.randint(-10000, 10000), random.randint(-10000, 10000))
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_out_of_range_2():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    obj1.cannon(random.randint(-10000, 10000), random.randint(-10000, 10000))
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result


def test_random_out_of_range_3():
    obj1 = Robot(
        position=(5, 10),
        direction=45,
    )
    obj1.current_velocity = 100
    obj1.current_damage = 100
    obj1.cannon(random.randint(-10000, 10000), random.randint(-10000, 10000))
    obj1._shoot()
    result= obj1.misil_position
    assert result[0] > -1 and result[0] < 1000 and result[1] > -1 and result[1] < 1000
    assert obj1.misil_position == result
