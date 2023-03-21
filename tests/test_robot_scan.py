from routers.robot.robot_class import Robot

def test_1():
    """
    Test 1: Los robots están en el mismo eje x,
            pero r2, está a 10m más arriba de r1.
    """
    r1 = Robot((500, 490), 90)
    r2 = Robot((500, 500), 90)
    r1.point_scanner(90, 10)
    r1._scan([r2.current_position])
    assert r1.scan_result == 10


def test_2():
    """
    Test 2: Los robots están en el mismo eje y,
            pero r2 está a 100m a la izquierda de r1.
    """
    r1 = Robot((500, 490), 90)
    r2 = Robot((400, 490), 90)
    r1.point_scanner(180, 10)
    r1._scan([r2.current_position])
    assert r1.scan_result == 100


def test_3():
    """
    Test 3: r2 está a 100m de distancia de r1, en el
            eje x e y, y en el margen inf der.
        Ejemplo:
            r1
                r2
    """
    r1 = Robot((500, 600), 90)
    r2 = Robot((600, 500), 90)
    r1.point_scanner(315, 9)
    r1._scan([r2.current_position])
    assert int(r1.scan_result) == 141


def test_4():
    """
    Test 4: r2 está a 100m de las posiciones x e y.
        Ejemplo:
                r2
            r1
    """
    r1 = Robot((500, 500), 90)
    r2 = Robot((600, 600), 90)
    r1.point_scanner(45, 9)
    r1._scan([r2.current_position])
    assert int(r1.scan_result) == 141


def test_5():
    """
    Test 5: r2 está  a 100m de las posiciones x e y.
        Ejemplo:
                r1
            r2
    """
    r1 = Robot((600, 600), 90)
    r2 = Robot((500, 500), 90)
    r1.point_scanner(225, 9)
    r1._scan([r2.current_position])
    assert int(r1.scan_result) == 141


def test_6():
    """
    Test 6: r2 está a más de 100m de distancia de r1, en el
            eje x e y, y en el margen inf der, por lo que con
            un rango de 10 en el escáner no llega a detectarlo.
        Ejemplo:
            r1
                r2
    """
    r1 = Robot((500, 600), 90)
    r2 = Robot((605, 500), 90)
    r1.point_scanner(315, 10)
    r1._scan([r2.current_position])
    assert int(r1.scan_result) == 145


def test_7():
    """
    Test 7: Trae la distancia mínima aunque dos robots estén en el rango.
    """
    r1 = Robot((500, 600), 90)
    r2 = Robot((600, 500), 90)
    r3 = Robot((610, 500), 90)
    r1.point_scanner(315, 9)
    r1._scan([r2.current_position, r3.current_position])
    r1.point_scanner(315, 9)
    assert int(r1.scan_result) == 141

def test_8():
    r1 = Robot((500, 600), 90)
    r2 = Robot((0, 0), 90)
    r1.point_scanner(315, 10)
    r1._scan([r2.current_position])
    assert int(r1.scan_result) == 1500