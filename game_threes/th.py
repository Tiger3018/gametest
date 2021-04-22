import game_threes, threading
from game_threes import text
from threading import Thread, Lock

lockTriggerMove = Lock()
lockDisplay = Lock()

def exceptHookOverride(args, /):
    exceptHookOrigin(args)
    text.logerror("Raise Exception, exit 1")
    game_threes.threadExit(1)
exceptHookOrigin = threading.excepthook
threading.excepthook = exceptHookOverride