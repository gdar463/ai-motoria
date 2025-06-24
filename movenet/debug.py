import time
import os
from enum import Enum

if "DEBUG" in os.environ:
  debug = int(os.environ["DEBUG"])
else:
  debug = 0

class DebugLevel(Enum):
  INFO = 0 # should not be used
  DEBUG = 1
  VERBOSE = 2

def trace(message: str, level: DebugLevel = DebugLevel.DEBUG):
  if debug >= level.value:
    print(f"{level.name}: {message}")

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