import pygame as pg
from . import PROGRAMMEDIA, text
from os.path import isfile
from abc import ABC

class clickObject(pg.sprite.Sprite):
    '''
    
    '''

class clickGroup(pg.sprite.Group):
    '''
    draw() : Like RenderUpdates but with desired change list
    '''
    def __init__(self, *sprites):
        pg.sprite.Group.__init__(sprites)
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

class card(pg.sprite.Sprite):
    imgStandard = {}
    def classInit():
        imgFormat = 'card{}.png'
        standardSize = (125, 175)
        suffixDict = {1 : '1', 2 : '2', 3 : '3', 6 : '6', 12 : '12', 24 : '24',
        48 : '48', 96 : '96', 192 : '192', 384 : '384', 768 : '768'}
        for pair in suffixDict.items():
            if not fileProcess.check(imgFormat.format(pair[1])):
                pair = (pair[0], '')
            listLink = card.imgStandard[pair[0]] = []
            listLink.append( fileProcess.imageObj(
                imgFormat.format(pair[1]), standardSize) )
    @staticmethod
    def merge(inst1, inst2):
        if not (isinstance(inst1, card) and isinstance(inst2, card)):
            raise TypeError("args must be game_threes.uidraw.card")
        if inst1.num != inst2.num:
            return False

    def __init__(self, num, pos, *groups):
        pg.sprite.Sprite(cardGroup, groups)
        if num not in card.imgStandard:
            textwarn("Pls check your card.num")
        if pos > 16:
            textwarn("Pls check your card.pos")
        self.num = num
        self.pos = pos
        self.image = card.imgStandard[num]
        self.rect = cardGroup.standardPos[pos]
    def draw(self):
        pass

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
    def __init__(self, *sprites):
        pg.sprite.Group.__init__(self, sprites)
    # standardSize = (125, 175) # debug use
    # def test(self, surface):
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[3])
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[4])
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[9])
    #     surface.blit(fileProcess.imageObj("card4.png", self.standardSize), self.standardPos[10])
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[14])

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

class fileProcess(ABC):
    def check(fileName):
        filePath = PROGRAMMEDIA + fileName
        isfile(filePath)
    def imageObj(fileName, size = None):
        fileObj = pg.image.load(PROGRAMMEDIA + fileName)
        if size:
            fileObj = pg.transform.smoothscale(fileObj, size)
        return fileObj


def uiUpdate(surface, frame):
    pass