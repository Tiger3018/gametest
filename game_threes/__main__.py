#!/bin/env python3

if not __package__ :
    from sys import path as _pathSys
    _pathSys.insert(0, '')
    __package__ = "game_threes"

import game_threes
import pygame_menu, threading, signal, ctypes
import pygame as pg
from . import uidraw, text, gen

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
    # keyHandle = threading.Thread(name = "keyHandle", target = gen.check)
    # Module, Event Init. Display & uidraw.card Init.
    th1 = threading.Thread(name = "eventHandle", target = eventHandler)
    th1.start()
    # Give mainThread some thing to do.
    uidraw.card.classInit()
    while True:
        sleep(10)
    # Event handler
                # if keyHandle
            # if event.type == pg.MOUSEBUTTONDOWN :
            #     pass

def eventHandler():
    pg.init()
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN, pg.KEYUP, pg.QUIT])
    # threading.Thread(name = "pygameEvent", target = pg.fastevent.init).start()
    pg.fastevent.init()

    # pg.display.quit()
    # pg.display.init()
    surface = pg.display.set_mode(game_threes.PROGRAMSIZE, vsync = 1)
    imTest = pg.transform.scale(pg.image.load("./media/bg.png"), game_threes.PROGRAMSIZE)
    surface.blit(imTest, (0, 0, 420, 600))
    pg.draw.rect(surface, (0, 255, 0), (300, 100, 10, 10))
    pg.display.flip()

    while event := pg.fastevent.wait() :
        # print(event)
        if event.type == pg.QUIT :
            text.loginfo("Successfully exit with pg.fastevent, exit 0")
            game_threes.threadExit(0)
        elif event.type == pg.KEYUP :
            directionKey = keyInterupt[event.key]
        pg.draw.rect(surface, (0, 255, 0), (200, 100, 10, 10))
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


