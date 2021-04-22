#!/bin/env python3.8

if not __package__ :
    from os import path as _pathOS
    from sys import path as _pathSys
    _pathSys.insert(0, _pathOS.dirname(__file__) + '/..')
    # print(_pathSys)
    __package__ = "game_threes"


import game_threes
import pygame_menu, signal, ctypes
import pygame as pg
pg.init()
from game_threes import text, status, uidraw, th
from traceback import print_exc
from time import sleep

def __main__():
    '''
    Environment initialization : winDPI, pygame, pygame_menu, game_threes.uidraw.card
    '''
    try:
        if game_threes.PLATFORMNAME == 'nt' :
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        text.logwarn("ctypes on win32 failed.")
    text.loginfo("__main__()")
    # Module, Event Init. Display & uidraw.card Init.
    th1 = th.Thread(name = "eventHandle", target = eventHandler)
    th2 = th.Thread(name = "displayHandle", target = uidraw.displayHandler, args = (60))
    th1.start()
    th2.start()
    # Give mainThread something to do.
    uidraw.card.classInit()
    while True:
        sleep(10)

def eventHandler():
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN, pg.KEYUP, pg.QUIT])
    pg.fastevent.init()
    keyPre = {
        0 : (pg.K_w, pg.K_UP), 3 : (pg.K_a, pg.K_LEFT), 2 : (pg.K_s, pg.K_DOWN),
        1 : (pg.K_d, pg.K_RIGHT), 4 : (pg.K_r)
        }
    keyInterpret = {k : v for v, kIter in keyPre.items() for k in kIter}
    while event := pg.fastevent.wait() :
        # print(event)
        try:
            if event.type == pg.QUIT :
                text.loginfo("Successfully exit with pg.fastevent, exit 0")
                game_threes.threadExit(0)
            elif event.type == pg.KEYUP :
                directionKey = keyInterpret.get(event.key)
                if directionKey <= 3:
                    if not thLockTriggerMove.acquire(blocking = False):
                        text.logwarn(
                            "Try to move <{}>, "\
                            "but trigger still running.".format((directionKey)))
                    elif not uidraw.thLockDisplay.acquire(blocking = False): # status - Locked
                        threading.Thread(
                            name = "TriggerMove",
                            target = trMove,
                            args = (directionKey)
                            ).start()
                        # do sth here
                    else:
                        text.logwarn(
                            "Try to move <{}>, "\
                            "but uidraw still running.".format((directionKey)))
                elif directionKey == 4:
                    raise NotImplementedError('restart game.')
        except Exception:
            print_exc()
        # pg.draw.rect(surface, (0, 255, 0), (200, 100, 10, 10))

def trMove(moveDir):
    thLockTriggerMove.acquire()
    if status.confirm(directionKey):
        status.check()
        thLockDisplay.release()
        # music implement
    else:
        text.logwarn("invalid direction.")
    thLockTriggerMove.release()

def exceptHookOverride(args, /):
    exceptHookOrigin(args)
    text.logerror("Raise Exception, exit 1")
    game_threes.threadExit(1)
exceptHookOrigin = threading.excepthook
threading.excepthook = exceptHookOverride

thLockTriggerMove = threading.Lock()
thLockDisplay = threading.Lock()

try:
    __main__()
except KeyboardInterrupt:
    print_exc()
    text.logwarn("SIGINT, exit -1")
except Exception:
    print_exc()
finally:
    game_threes.threadExit(-1)

# print(globals(), vars())

# from importlib.util import spec_from_file_location, module_from_spec
# # importlib.import_module("..game_threes", "game_threes")
# spec = spec_from_file_location("game_threes", "../game_threes/__init__.py")
# spec.loader.exec_module(module_from_spec( spec ))

# if __name__ == "__main__":
#     __init__()


