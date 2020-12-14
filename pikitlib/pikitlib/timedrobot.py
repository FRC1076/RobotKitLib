#from iterativerobotbase import IterativeRobotBase
from .iterativerobotbase import IterativeRobotBase

class TimedRobot(IterativeRobotBase):
    def __init__(self):
        IterativeRobotBase.__init__(self)
        pass
if __name__ == "__main__": #testing
    r = TimedRobot()