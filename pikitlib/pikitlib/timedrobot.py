#from iterativerobotbase import IterativeRobotBase
from .iterativerobotbase import IterativeRobotBase

class TimedRobot(IterativeRobotBase):
    def __init__(self):
        super().__init__()
        pass
if __name__ == "__main__": #testing
    r = TimedRobot()