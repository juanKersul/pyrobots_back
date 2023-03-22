from routers.robot.robot_class import Robot

class default1(Robot):
    def initialize(self):
        pass
    def respond(self):
        direction = self.get_direction()
        distance= self.scanned()
        if(direction==0):
            self.drive(90,50)
            self.point_scanner(90,5)
            if(distance<1500):
                self.cannon(0,distance)
        elif(direction==90):
            self.drive(180,50)
            self.point_scanner(180,5)
            if(distance<1500):
                self.cannon(90,distance)
        elif(direction==180):
            self.drive(270,50)
            self.point_scanner(270,5)
            if(distance<1500):
                self.cannon(180,distance)
        elif(direction==270):
            self.drive(0,50)
            self.point_scanner(0,5)
            if(distance<1500):
                self.cannon(270,distance)
        else:
            self.drive(0,50)