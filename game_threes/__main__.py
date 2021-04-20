#!/bin/env python3.8

if not __package__ :
    from os import path as _pathOS
    from sys import path as _pathSys
    _pathSys.insert(0, _pathOS.dirname(__file__) + '/..')
    # print(_pathSys)
    __package__ = "game_threes"


import game_threes
import pygame_menu, threading, signal, ctypes
import pygame as pg
pg.init()
from game_threes import uidraw, text, status

def __main__():
    '''
    Environment initialization : winDPI, pygame, pygame_menu, game_threes.uidraw.card
    '''
    keyInterrupt = {}
    try:
        if game_threes.PLATFORMNAME == 'nt' :
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        text.logwarn("ctypes on win32 failed.")
    text.loginfo("__main__()")
    # Module, Event Init. Display & uidraw.card Init.
    th1 = threading.Thread(name = "eventHandle", target = eventHandler)
    th1.start()
    # Give mainThread something to do.
    uidraw.card.classInit()
    while True:
        sleep(10)

def eventHandler():
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN, pg.KEYUP, pg.QUIT])
    pg.fastevent.init()
    uidraw.card.classInit()

    # pg.display.quit()
    # pg.display.init()
    surface = pg.display.set_mode(game_threes.PROGRAMSIZE, vsync = 1)
    imTest = pg.transform.scale(pg.image.load("./media/bg.png"), game_threes.PROGRAMSIZE)
    surface.blit(imTest, (0, 0, 420, 600))
    pg.draw.rect(surface, (0, 255, 0), (300, 100, 10, 10))
    pg.display.flip()

    test = uidraw.card(3, 4)
    test.draw(surface)
    while event := pg.fastevent.wait() :
        # print(event)
        if event.type == pg.QUIT :
            text.loginfo("Successfully exit with pg.fastevent, exit 0")
            game_threes.threadExit(0)
        elif event.type == pg.KEYUP :
            directionKey = keyInterupt[event.key]
        # pg.draw.rect(surface, (0, 255, 0), (200, 100, 10, 10))
        pg.display.flip()

def exceptHookOverride(args, /):
    exceptHookOrigin(args)
    text.logerror("Raise Exception, exit 1")
    game_threes.threadExit(1)
exceptHookOrigin = threading.excepthook
threading.excepthook = exceptHookOverride

from traceback import print_exc
from time import sleep
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


