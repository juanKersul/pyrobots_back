from routers.robot.robot_class import Robot
from typing import Optional
from random import randint


class default2(Robot):
    round: int
    state: Optional[str]

    def initialize(self):
        self.round = 0
        self.state = None
        self.searching_last_direction = None
        self.last_scan = None

    def respond(self):
        try:
            if self.state is None:
                self.state = "searching"
                self.searching_last_direction = randint(0, 360)
                self.point_scanner(self.searching_last_direction, 1)
            elif self.state == "searching":
                self.last_scan = self.scanned()
                if self.last_scan == 1500:
                    self.searching_last_direction += 10
                    self.point_scanner(self.searching_last_direction, 1)
                elif self.last_scan > 100:
                    self.state = "moving and attacking"
                    self.drive(self.searching_last_direction, 50)
                    self.cannon(self.searching_last_direction, self.last_scan)
                    self.point_scanner(self.searching_last_direction, 1)
                else:
                    self.state = "attacking"
                    self.drive(self.searching_last_direction, 0)
                    self.point_scanner(self.searching_last_direction, 1)
            elif self.state == "moving and attacking":
                self.last_scan = self.scanned()
                if self.last_scan == 1500:
                    self.state = "searching"
                    self.searching_last_direction += 10
                    self.point_scanner(self.searching_last_direction, 1)
                elif self.last_scan > 100:
                    self.drive(self.searching_last_direction, 50)
                    self.cannon(self.searching_last_direction, self.last_scan)
                    self.point_scanner(self.searching_last_direction, 1)
                else:
                    self.state = "attacking"
                    self.drive(self.searching_last_direction, 0)
                    self.point_scanner(self.searching_last_direction, 1)
            elif self.state == "attacking":
                self.cannon(self.searching_last_direction, self.last_scan)
                self.last_scan = self.scanned()
                if self.last_scan == 1500:
                    self.state = "searching"
                    self.searching_last_direction += 10
                self.point_scanner(self.searching_last_direction, 1)

            self.round += 1
        except Exception as e:
            print(e)
