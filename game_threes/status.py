from game_threes.uidraw import cardGroupInstance as cgObj

class _gameStatus:
    '''
    ** self.predict : list, length = 4 **
    Each subobject will be None or [WillAdd, WillDel, WillMove], without nextHold.
    WillAdd, WillDel : [pos, num]
    WillMove : [dir, card]
    '''
    moveFind = [
        [None, None, None, None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        [1, 2, 3, None, 5, 6, 7, None, 9, 10, 11, None, 13, 14, 15, None],
        [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, None, None, None, None],
        [None, 0, 1, 2, None, 4, 5, 6, None, 8, 9, 10, None, 12, 13, 14]]
    dirReverse = [2, 3, 0, 1]
    def __init__(self):
        self._reset()
    def _reset(self):
        self.predict = [None for i in range(4)]
    def _move(self, posAt, moveDir, mN):
        # mN = _gameStatus.moveFind[moveDir]
        # mNO = gameStatus.moveFind[dirReverse[moveDir]]
        if not posAt:
            return []
        recurValue = self._move(mN[posAt], moveDir, mN)
        if cardObj := cgObj.find(posAt):
            return [[_gameStatus.dirReverse[moveDir], cardObj]] + recurValue
        else:
            return recurValue 
    def _merge(self, posAt, moveDir, mN):
        # mN = _gameStatus.moveFind[moveDir]
        if not posAt:
            return []
        elif not (cardObj := cgObj.find(posAt)):
            return [None, None, self._move(mN[posAt], moveDir, mN)]
        elif newNumber := cardObj.merge(cgObj.find(mN[posAt])):
            pass
        else:
            return self._merge(mN[posAt], moveDir, mN)
    def _dirCheck():
        dirInit = [[12, 13, 14, 15], [0, 4, 8, 12], [0, 1, 2, 3], [3, 7, 11, 15]]

def nextHold():
    '''
    Prepare status for user's choice, whether first or following steps.
    '''
    if not currentStatus:
        currentStatus = _gameStatus()
    currentStatus.nextHold()

def check():
    matchDict = {0 : 'w', 1 : 'd', 2 : 's', 3 : 'a'}
    if not isinstance(currentStatus, _gameStatus):
        raise TypeError("Get currentStatus failed.")
    if returnValue := currentStatus.check():
        return returnValue
    else:
        return False

def confirm(dir):
    pass