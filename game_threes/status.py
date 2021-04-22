import game_threes
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
    WillMove : [dir, card] * MAY HAVE WillDel * MUST follow the step
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
        self.nextCard = None
        self.sample = [None for i in range(4)]

    def _move(self, posAt, moveDir, mN):
        # mN = _gameStatus.moveFind[moveDir]
        # mNO = gameStatus.moveFind[dirReverse[moveDir]]
        # print("_move", posAt, moveDir, self)
        if posAt == None:
            return []
        recurValue = self._move(mN[posAt], moveDir, mN)
        if cardObj := cgObj.find(posAt):
            # if not recurValue:
                # recurValue = []
            return [(_gameStatus.dirReverse[moveDir], cardObj)] + recurValue
        else:
            return recurValue 

    def _merge(self, posAt, moveDir, mN):
        '''
        0 == False, None == False. SO USE xx == None
        LINE - along the given direction
        1. If find(posAt) == None THEN any other card in this line may just move.
        2. If posAt is the final card THEN this line can't move.
        3. If find(mN[posAt]) == None THEN from this card
        '''
        # mN = _gameStatus.moveFind[moveDir]
        # print("_m", posAt, moveDir, self)
        if not (cardObj := cgObj.find(posAt)):
            if recurValue := self._move(mN[posAt], moveDir, mN):
                return [[], [], recurValue]
            else:
                return True # There is no card in this direction
        elif mN[posAt] == None:
            return False # There are full cards that can't be merged.
        elif newNumber := cardObj.merge(moveCardObj := cgObj.find(mN[posAt])):
            return [
                [(posAt, newNumber)],
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
            sampleTemp = []
            dirSelectR = _gameStatus.dirReverse[dirSelect]
            mN = _gameStatus.moveFind[dirSelectR]
            for dirInitSelect in _gameStatus.dirInit[dirSelectR]:
                if recurValue := self._merge(dirInitSelect, dirSelectR, mN): # not False
                    if not recurValue == True:
                        for i in range(3):
                            predictTemp[i] += recurValue[i]
                    predictTemp[3] += 1 # this direction of line can be moved
                    sampleTemp.append(dirInitSelect)
            genNextValue = min(genNextValue, predictTemp[3])
            self.sample[dirSelectR] = sampleTemp
            if predictTemp[2]: # must move one exist card at least.
                self.predict[dirSelect] = predictTemp[:3]
                returnValue += [dirSelect]
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
    return currentStatus.check()
    # currentStatus.check()

def check():
    '''
    After a display UPDATE, it will be called to examine the game status.
    '''
    if not isinstance(currentStatus, _gameStatus):
        raise TypeError("Get currentStatus failed.")
    return currentStatus.check()

def confirm(moveDir):
    global renderQueue
    game_threes.text.logdebug(currentStatus.predict)
    if not (predict := currentStatus.predict[moveDir]):
        return False
    moveList = []
    sampleList = currentStatus.sample[moveDir]
    # FIRST  - DELETE
    renderQueue += [(None, it[1]) for it in predict[1]] 
    # SECOND - MOVE
    for it in predict[2]:
        if not (posTo := _gameStatus.moveFind[it[0]][it[1].pos]) == None:
            moveList.append((posTo, it[1]))
    renderQueue += moveList 
    # THIRD  - ADD
    randomList = random.sample(sampleList, len(sampleList))
    cardInstance = [card(it[1], it[0]) for it in predict[0]] + \
        [card(currentStatus.nextCard[i], randomList[i]) \
         for i in range(len(currentStatus.nextCard))]
    renderQueue += [(cardGroupInstance, it) for it in cardInstance] 
    game_threes.text.logdebug("confirm({}) completed".format(moveDir), renderQueue)
    return True

currentStatus = None