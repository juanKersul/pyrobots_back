from game.Robot import GameRobot


class BaseGame:
    def __init__(self, robots: list[GameRobot], rules: dict):
        self.robots = robots
        self.rules = rules
        self.results = []

    def run(self, rounds):
        for robot in self.robots:
            robot.initialize()
        for i in range(rounds):
            for robot in self.robots:
                robot.respond()
            for robot in self.robots:
                robots_copy = self.robots.copy()
                other_robots = robots_copy.remove(robot)
                other_robots_pos = [r.get_position() for r in other_robots]
                robot.scan(other_robots_pos)
            for robot in self.robots:
                robot.shoot()
            for robot in self.robots:
                robot.move()
            for robot in self.robots:
                robots_copy = self.robots.copy()
                other_robots = robots_copy.remove(robot)
                other_robots_misil_position = [
                    r.get_misil_position() for r in other_robots
                ]
                robot.get_damage(other_robots_misil_position, 20, 5)
            self.results.append(
                {
                    "round": i,
                    "results": [r.get_atributes() for r in self.robots],
                }
            )

    def get_results(self):
        return self.results
