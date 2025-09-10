import os
import time
from enum import Enum

from colorama import Fore, just_fix_windows_console

just_fix_windows_console()


class MessageLevel(Enum):
    ERROR = (-1, Fore.LIGHTRED_EX)
    INFO = (0, Fore.LIGHTBLUE_EX)
    VERBOSE = (1, Fore.LIGHTGREEN_EX)
    DEBUG = (2, Fore.LIGHTMAGENTA_EX)
    VERY_VERBOSE = (3, Fore.LIGHTYELLOW_EX)


class LoggerClass:
    def __init__( self, level ):
        if level:
            self.level = level
        else:
            if "DEBUG" in os.environ:
                self.level = int(os.environ["DEBUG"])
            else:
                self.level = 0

    def trace( self, message: str, level: MessageLevel = MessageLevel.DEBUG ):
        if self.level >= level.value[0]:
            print(f"{level.value[1]}{level.name}{Fore.RESET}: {message}")


logger = LoggerClass(None)


class Timing:
    def __init__( self, message ):
        self.message = message

    def __enter__( self ):
        logger.trace(f"started timing {self.message}")
        self.start = time.time()
        return self

    def __exit__( self, exc_type, exc_value, traceback ):
        self.end = time.time()
        logger.trace(f"{self.message} timing: {self.end - self.start}")

    def force_end( self ):
        self.__exit__(None, None, None)
