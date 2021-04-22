'''
** game_threes.uidraw **
PLEASE CALL pygame.init() BEFORE IMPORT THIS FILE
This file has 1 abstracted class : fileprocess. (-> captionObject)
By import this file -> clickGroupInstance, cardGroupInstance.
By starting a thread calling function displayHandler, it will interact with sprite system.
'''
import pygame as pg
from game_threes import PROGRAMSIZE, PROGRAMMEDIA, SIZEALL
from game_threes import text, th
from os.path import isfile
from abc import ABC

class fileProcess(ABC):
    def check(fileName):
        filePath = PROGRAMMEDIA + fileName
        return isfile(filePath)
    def imageObj(fileName, size = None):
        fileObj = pg.image.load(PROGRAMMEDIA + fileName)
        if size:
            fileObj = pg.transform.smoothscale(fileObj, size)
        return fileObj
    def fontObj(fileName, size = 60):
        fileObj = pg.font.Font(PROGRAMMEDIA + fileName, size)
        return fileObj

captionObject = fileProcess.fontObj("RocknRollOne-Regular.ttf")

class clickObject(pg.sprite.Sprite):
    '''
    
    '''

class clickGroup(pg.sprite.Group):
    '''
    draw() : Like RenderUpdates but with desired change list
    '''
    def __init__(self, *sprites):
        pg.sprite.AbstractGroup.__init__(self)
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
    '''
    __init__(num : int, pos : int(0 - 15), *groups)
    '''
    imgStandard = {}
    @staticmethod
    def classInit():
        '''
        Prepare imgStandard : dict which is used by each card.
        '''
        imgFormat = 'card{}.png'
        standardSize = (125, 175)
        suffixDict = {1 : '1', 2 : '2', 3 : '3', 6 : '6', 12 : '12', 24 : '24',
        48 : '48', 96 : '96', 192 : '192', 384 : '384', 768 : '768'}
        for pair in suffixDict.items():
            listLink = card.imgStandard[pair[0]] = [ None ]
            if not fileProcess.check(imgFormat.format(pair[1])):
                pair = (pair[0], '') # fall back to empty filename 'card.png'
                listLink.append("fallback")
            listLink[0] = fileProcess.imageObj(
                imgFormat.format(pair[1]),
                standardSize
                ) 

    def __init__(self, num, pos, *groups):
        if num not in card.imgStandard:
            text.logwarn("Pls check your card.num")
        if pos >= SIZEALL:
            text.logwarn("Pls check your card.pos")
        self._num = num
        self._pos = pos
        self.image = card.imgStandard[num]
        self.rect = cardGroup.standardPos[pos]
        pg.sprite.Sprite.__init__(self, [cardGroupInstance, groups])

    def __del__(self):
        self.kill()

    def draw(self, surface):
        rect = surface.blit(self.image[0], self.rect)
        if self.image[1] == "fallback" :
            r2 = surface.blit(
                captionObject.render(str(self.num), True, (0, 0, 0)),
                self.rect
                )
        return rect

    def merge(self, waitS : [pg.sprite.Sprite, None]):
        if not waitS:
            return False
        num = waitS.num
        if not num or self._num != num:
            return False
        elif self._num + num == 3:
            return 3
        else:
            return self._num * 2

    def move(self, posTo):
        self.groups()[0].move_sprite_internal(self, posTo)
        '''
        for group in self.groups():
            try:
                group.move_sprite_internal(self, posTo)
            except AttributeError:
                text.logwarn("self.move() meets invalid group {}.".format(group))
        '''
    
    @property
    def num(self):
        return self._num

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value):
        if pos >= SIZEALL:
            raise ValueError("")
        self.rect = cardGroup.standardPos[value]
        self._pos = value

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
        pg.sprite.Group.__init__(self, sprites) # TOBERAISE
        self._changedSprites = []
        self._posObject = [None for i in range(SIZEALL)]
    # standardSize = (125, 175) # debug use
    # def test(self, surface):
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[3])
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[4])
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[9])
    #     surface.blit(fileProcess.imageObj("card4.png", self.standardSize), self.standardPos[10])
    #     surface.blit(fileProcess.imageObj("card.png", self.standardSize), self.standardPos[14])

    def add_internal(self, sprite, layer = None):
        pg.sprite.Group.add_internal(self, sprite, layer)
        self._changedSprites += [sprite]
        self._setPosObj(sprite, sprite.pos)

    def remove_internal(self, sprite):
        pg.sprite.Group.remove_internal(self, sprite)
        self._delPosObj(sprite.pos)
     
    def _setPosObj(self, sprite, posAt):
        if self._posObject[posAt]:
            raise RuntimeError("cardGroup : one sprite overide pos {}".format(posAt))
            # text.logerror("Overide pos {}".format(posAt))
        else:
            self._posObject[posAt] = sprite

    def _delPosObj(self, posAt):
        if not self._posObject[posAt]:
            raise RuntimeError("cardGroup : pos {} is already None".format(posAt))
        else:
            self._posObject[posAt] = None

    def move_sprite_internal(self, sprite, posTo):
        # if sprite not in self:
            # raise RuntimeError("move_sprite() failed.")
        self._delPosObj(sprite.pos)
        sprite.pos = posTo
        self._setPosObj(sprite, sprite.pos)

    def stepOver(self, sprite, *rect):
        pass

    def draw(self, surface : pg.surface):
        surface_blit = surface.blit
        dirty_append = dirty.append
        dirty = self.lostsprites
        self.lostsprites = []
        for sprite in self._changedSprites:
            old_rect = self.spritedict[sprite]
            new_rect = surface_blit(sprite.image, sprite.rect)
            if old_rect:
                if new_rect.colliderect(old_rect):
                    dirty_append(new_rect.union(old_rect))
                else:
                    dirty_append(new_rect)
                    dirty_append(old_rect)
            else:
                dirty_append(new_rect)
            self.spritedict[sprite] = new_rect
        self._changedSprites = []
        return dirty

    def find(self, posAt):
        if posAT < SIZEALL:
            return self._posObject[posAt]
        else:
            return None

clickGroupInstance = clickGroup()
cardGroupInstance = cardGroup()
renderQueue = []

def displayHandler(surface = None, frame = 60):
    global renderQueue
    from game_threes.status import check as status_check
    from game_threes.status import nextHold as status_nextHold
    
    surface = pg.display.set_mode(PROGRAMSIZE, vsync = 1)
    imTest = pg.transform.scale(fileProcess.imageObj("bg.png"), PROGRAMSIZE)
    surface.blit(imTest, (0, 0, 420, 600))
    pg.draw.rect(surface, (0, 255, 0), (300, 100, 10, 10))
    card.classInit()
    # test = card(3, 4)
    # test = card(6, 5)
    # test = card(3, 6)
    test = card(1, 7)
    status_nextHold()
    test.draw(surface)

    while True:
        if th.lockDisplay.locked():
            pg.fastevent.post(pg.fastevent.wait()) # a better thread.
            continue
        if not renderQueue:
            pg.display.flip()
        else:
            renderTemp = renderQueue
            renderQueue = []
            rectUpdate = []
            surface.blit(imTest, (0, 0, 420, 600))
            for reIt in renderTemp: # [Object has draw()], (group, sprite), (pos, sprite), (None, sprite)
                lenreIt = len(reIt)
                if lenreIt == 1:
                    rectUpdate.append(reIt.draw(surface))
                elif lenreIt == 2:
                    if isinstance(reIt[0], pg.sprite.Group):
                        reIt[0].add(reIt[1])
                    elif reIt[0]:
                        reIt[0].move(pos)
                    else:
                        del reIt[0]
            pg.display.update(rectUpdate)
            status_check()
        th.lockDisplay.acquire()
# if threading.current_thread().getName() == "displayHandle":