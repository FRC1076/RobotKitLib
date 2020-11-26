import sys
import threading
import time
import logging

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        print( "base init", file=sys.stderr )
        super(StoppableThread, self).__init__()
        self._stopper = threading.Event()          

    def stopit(self):                            
        print( "base stop()", file=sys.stderr )
        self._stopper.set()                        

    def stopped(self):
        return self._stopper.is_set()              

class datalogger(StoppableThread):
    """
    """

    import time

    def __init__(self):
      """
      """
      StoppableThread.__init__(self)
      
      print( "thread init", file=sys.stderr )

    def run(self):
      """
      """
      print( "thread running", file=sys.stderr )
      while not self.stopped():
        print("running")
        time.sleep(0.33)
      print( "thread ending", file=sys.stderr )


test = datalogger()
test.start()
time.sleep(3)
logging.debug("stopping thread")
test.stopit()                                      
logging.debug("waiting for thread to finish")
test.join()
