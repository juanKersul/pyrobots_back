from routers.game.game import inflingir_danio
from routers.robot.robot_class import Robot

def test_colision():
    robot1= Robot((100,100),90)
    robot2= Robot((100,100),90)
    inflingir_danio(robot1,[robot2])
    assert robot1.current_damage == 98 and robot2.current_damage == 98

def test_Wallcolision():
    robot1= Robot((0,0),90)
    inflingir_danio(robot1,[])
    assert robot1.current_damage == 98 

def test_misilImpact():
    robot1= Robot((500,500),90)
    robot2= Robot((100,100),90)
    robot2.misil_position = (500,500)
    inflingir_danio(robot1,[robot2])
    assert robot1.current_damage == 90

def test_badInput():
    robot1= Robot((500,500),90)
    inflingir_danio(robot1,[])
    assert True

