import time
import os

if "DEBUG" in os.environ:
  debug = os.environ

def trace(message: str):
  if debug:
    print(message)

class Timing:
  def __init__( self, message ):
    self.message = message

  def __enter__( self ):
    trace(f"started timing {self.message}")
    self.start = time.time()
    return self

  def __exit__( self, exc_type, exc_value, traceback ):
    self.end = time.time()
    trace(f"{self.message} timing: {self.end - self.start}")

  def force_end( self ):
    self.__exit__( None, None, None )