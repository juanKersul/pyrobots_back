from routers.game.game import avanzar_ronda
from routers.robot.robot_class import Robot


def test_avanzar_ronda():
    class robotjuan(Robot):
        def initialize(self):
            a = a

        def respond(self):
            self.cannon(20, 300)
            self.drive(100, 80)

    juan = robotjuan((1, 1), 0)
    fede = robotjuan((1, 990), 0)
    alexis = robotjuan((100, 200), 0)
    carlos = robotjuan((990, 990), 0)
    res = avanzar_ronda([juan, fede, alexis, carlos])

    assert len(res) == 4

def test_avanzar_ronda2():
    class robotjuan(Robot):
        def initialize(self):
            a = a

        def respond(self):
            self.cannon(20, 300)
            self.drive(100, 80)


    alexis = robotjuan((100, 200), 0)
    carlos = robotjuan((990, 990), 0)
    res = avanzar_ronda([alexis, carlos])

    assert len(res) == 2
