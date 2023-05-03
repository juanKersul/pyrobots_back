from math import pi
from math import sin
from math import cos
from math import sqrt


def distance(t1: tuple, t2: tuple):
    res = round(sqrt((t2[0] - t1[0]) ** 2 + (t2[1] - t1[1]) ** 2))
    return res


def polar_to_rect(ang, distance, origin):
    radian = float(ang * pi / 180)
    x = round(origin[0] + distance * cos(radian))
    y = round(origin[1] + distance * sin(radian))
    if x <= 0:
        x = 0
    if x >= 999:
        x = 999
    if y <= 0:
        y = 0
    if y >= 999:
        y = 999
    return (x, y)


def amplitude_to_depth(degre):
    result = -7.5 * (degre * 9) + 867
    return round(result)
