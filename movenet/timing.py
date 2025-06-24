import time


class Timing:
  def __init__( self, message ):
    self.message = message
    pass

  def __enter__( self ):
    self.start = time.time()

  def __exit__( self, exc_type, exc_value, traceback ):
    self.end = time.time()
    print(f"{self.message}: {self.end - self.start}")
