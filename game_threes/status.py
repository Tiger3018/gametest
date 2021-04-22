from game_threes.uidraw import cardGroupInstance as cgObj
from game_threes.uidraw import renderQueue, card, cardGroupInstance
from bisect import bisect_left
import random

class _gameStatus:
    '''
    ** self.predict : list, length = 4 **
    Each subobject will be None or [WillAdd, WillDel, WillMove], without nextHold.
    WillAdd : [pos, num]
    WillDel : [pos, card]
    WillMove : [dir, card] * MAY HAVE WillDel
    '''
    moveFind = (
        (None, None, None, None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        (1, 2, 3, None, 5, 6, 7, None, 9, 10, 11, None, 13, 14, 15, None),
        (4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None, None, None, None),
        (None, 0, 1, 2, None, 4, 5, 6, None, 8, 9, 10, None, 12, 13, 14))
    dirReverse = (2, 3, 0, 1)
    dirInit = ((12, 13, 14, 15), (0, 4, 8, 12), (0, 1, 2, 3), (3, 7, 11, 15))

    def __init__(self):
        self.verbose = -1
        self._reset()

    def _reset(self):
        self.predict = [None for i in range(4)]
        self.verbose += 1
        # self.nextCard

    def _move(self, posAt, moveDir, mN):
        # mN = _gameStatus.moveFind[moveDir]
        # mNO = gameStatus.moveFind[dirReverse[moveDir]]
        if not posAt:
            return []
        recurValue = self._move(mN[posAt], moveDir, mN)
        if cardObj := cgObj.find(posAt):
            return [(_gameStatus.dirReverse[moveDir], cardObj)] + recurValue
        else:
            return recurValue 

    def _merge(self, posAt, moveDir, mN):
        # mN = _gameStatus.moveFind[moveDir]
        if not posAt:
            return False
        elif not (cardObj := cgObj.find(posAt)):
            return [[], [], self._move(mN[posAt], moveDir, mN)]
        elif newNumber := cardObj.merge(moveCardObj := cgObj.find(mN[posAt])):
            return [
                (posAt, newNumber),
                [(mN[posAt], moveCardObj), (posAt, cardObj)],
                self._move(mN[posAt], moveDir, mN)
            ]
        else:
            return self._merge(mN[posAt], moveDir, mN)

    def check(self):
        self._reset()
        returnValue = []
        genNextValue = 2
        for dirSelect in range(4):
            predictTemp = [[], [], [], 0]
            dirSelectR = _gameStatus.dirReverse[dirSelect]
            mN = _gameStatus.moveFind[dirSelectR]
            for dirInitSelect in _gameStatus.dirInit[dirSelectR]:
                if recurValue := self._merge(dirInitSelect, dirSelectR, mN): # not False
                    for i in range(3):
                        predictTemp[i] += [recurValue[i]]
                    predictTemp[3] += 1
            if predictTemp[0]:
                self.predict[dirSelect] = predictTemp[:2]
                returnValue += dirSelect
                genNextValue = min(genNextValue, predictTemp[3])
        self.genNext(genNextValue)
        return returnValue

    def genNext(self, maxCard):
        rule = (0.2, 0.4, 0.9, 1)
        ruleNum = (1, 2, 3, 6)
        random.seed()
        ruleSelected = bisect_left(rule, random.random())
        self.nextCard = [ ruleNum[ruleSelected] ]


def nextHold():
    '''
    Prepare status for user's choice, whether first or following steps.
    '''
    global currentStatus
    if not currentStatus:
        currentStatus = _gameStatus()
    # currentStatus.check()

def check():
    '''
    After a display UPDATE, it will be called to examine the game status.
    '''
    if not isinstance(currentStatus, _gameStatus):
        raise TypeError("Get currentStatus failed.")
    return currentStatus.check()

def confirm(moveDir):
    if not (predict := currentStatus.predict[moveDir]):
        return False
    renderQueue.append(predict[2])
    renderQueue.append((None, it[1]) for it in predict[1])
    randomList = random.sample(currentStatus.dirInit[moveDir], 4)
    cardInstance = [card(it[1], it[0]) for it in predict[0]] + \
        [card(num, pos) for num in currentStatus.nextCard for pos in randomList]
    renderQueue.append([(cardGroupInstance, it) for it in cardInstance])
    pass

currentStatus = None