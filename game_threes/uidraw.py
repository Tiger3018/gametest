print(__package__)
import pygame as pg
from . import PROGRAMMEDIA

class clickObject(pg.sprite.Sprite):
    '''
    
    '''

class clickGroup(pg.sprite.Group):
    '''
    draw() : Like RenderUpdates but with desired change list
    '''
    def __init__(self, *sprites):
        pg.sprite.Group.__init__(self, sprites)
        self.changedSprites = sprites

    def update(self):
        pass
    def add(self, *sprites):
        raise NotImplementedError("ClickGroup can't add the sprite")
    def remove(self, *sprites):
        raise NotImplementedError("ClickGroup can't remove the sprite")

    def draw(self, surface : pg.surface):
        surface_blit = surface.blit
        dirty_append = dirty.append
        dirty = []
        for sprite in self.changedSprites:
            rect_i = self.spritedict[sprite] = surface_blit(sprite.image, sprite.rect)
            dirty_append(rect_i)
        self.changedSprites = []
        return dirty

class cardGroup(pg.sprite.Group):
    '''
    draw() : Like RenderUpdates but with desired change list
    130 - 705 = 25 * 3 + 125 * 4 ( 130 )
    285 - 1050 = 25 * 3 + 175 * 4
     = 10 * 3 + 65 * 4
    '''
    standardPos = ((130, 285), (280, 285), (430, 285), (580, 285),
                   (130, 485), (280, 485), (430, 485), (580, 485),
                   (130, 685), (280, 685), (430, 685), (580, 685),
                   (130, 885), (280, 885), (430, 885), (580, 885))
    standardSize = (125, 175)
    def __init__(self, *sprites):
        pg.sprite.Group.__init__(self, sprites)
    def test(self, surface):
        surface.blit(imageObj("card.png", self.standardSize), self.standardPos[3])
        surface.blit(imageObj("card.png", self.standardSize), self.standardPos[4])
        surface.blit(imageObj("card.png", self.standardSize), self.standardPos[9])
        surface.blit(imageObj("card4.png", self.standardSize), self.standardPos[10])
        surface.blit(imageObj("card.png", self.standardSize), self.standardPos[14])

    def stepOver(self):
        pass
    def draw(self, surface : pg.surface):
        surface_blit = surface.blit
        dirty_append = dirty.append
        dirty = []
        for sprite in self.changedSprites:
            rect_i = self.spritedict[sprite] = surface_blit(sprite.image, sprite.rect)
            dirty_append(rect_i)
        self.changedSprites = []
        return dirty

def imageObj(fileName, size = None):
    fileObj = pg.image.load(PROGRAMMEDIA + fileName)
    if size:
        fileObj = pg.transform.smoothscale(fileObj, size)
    return fileObj


def uiUpdate(surface, frame):
    pass