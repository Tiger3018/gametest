# Tiger3018 - MIT License
from os import name as PLATFORMNAME

PROGRAMSIZE = (835, 1200)
PROGRAMMEDIA = "./media/"

import pygame as pg
import pygame_menu, threading, ctypes
from . import const, uidraw, text


def __main__():
    try:
        if PLATFORMNAME == 'nt' :
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        text.logwarn("ctypes on win32 failed.")
    text.loginfo("__main__()")
    pg.init()
    surface = pg.display.set_mode(PROGRAMSIZE, flags = pg.SCALED)
    # print(name)
    imTest = pg.transform.scale(pg.image.load("./media/bg.png"), PROGRAMSIZE)
    surface.blit(imTest, (0, 0, 420, 600))
    pg.draw.rect(surface, (0, 255, 0), (300, 100, 10, 10))
    uidraw.cardGroup().test(surface)
    pg.display.flip()

    loopStatus = True
    pg.fastevent.init()
    newHandle = threading.Thread(name = "T1", target = __main__)
    # newHandle.start()
    while loopStatus : 
        for event in pg.fastevent.get() :
            if event.type == pg.MOUSEBUTTONDOWN :
                pass
            if event.type == pg.QUIT :
                exit()

    # menu = pygame_menu.Menu('Welcome', 300, 400, 
    #                       theme=pygame_menu.themes.THEME_BLUE)

    # menu.add.text_input('Name :', default='John Doe')
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    # get = menu.add.button('Play', start_the_game)
    # menu.add.button('Quit', pygame_menu.events.EXIT)
    # menu.mainloop(surface)

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass

# print(__name__, vars())
__main__()
