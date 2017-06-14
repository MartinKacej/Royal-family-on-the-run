# Royal family on the run
# Kralovska rodina na uteku
#
# Martin Kacej 2017
#

import copy


# -----Constants
King = 90
Queen = 50
Prince = 40
Chest = 30
Safe = 10
# --------

inf_State = True
inf_Traceback = True


class Rules:
    def checkPossibleMove(self, upper, lower):
        '''Checks if is possible to exchange basket from tower with basket from ground,
         e.g. weigth is between 0 and Safe constant'''
        assert (len(upper) > 0 or len(lower) > 0)
        upperWeight = self.calculateWeight(upper)
        lowerWeight = self.calculateWeight(lower)
        if (upperWeight == Chest) and (lowerWeight == 0):
            return True
        if 0 < (upperWeight - lowerWeight) <= Safe:
            return True
        return False

    def calculateWeight(self, tup):
        '''Sum of the given basket(list with max two items)'''
        assert 0 <= len(tup) <= 2
        weight = 0
        for i in tup:
            weight += i
        return weight
# ---------


class State:
    __tower = []
    __ground = []
    __g = 0
    __rules = Rules()
    __prevNode = None

    def __init__(self, up, down):
        self.__tower = up[:]
        self.__ground = down[:]

    def getTower(self):
        return self.__tower

    def getGround(self):
        return self.__ground

    def getPrevious(self):
        return self.__prevNode

    def setPrevious(self, p):
        self.__prevNode = p

    def increaseLevel(self):
        self.__g += 1

    def getLevel(self):
        return self.__g

    def setLevel(self, l):
        self.__g = l

    def getF(self):
        '''Returns value of heuristic function f(i).
        f(i) = h(i) + g(i)'''
        h = 0
        for i in self.__tower:
            h += (i/10)
        return self.__g + h

    def expandState(self):
        '''Calculate all possible states from current and return list of them'''
        expanded = []
        currentCopy = copy.deepcopy(self)
        t = self.getTuples(currentCopy.getTower())
        g = self.getTuples(currentCopy.getGround())
        g.append([0, 0])  # Dirty hack
        for it in t[:]:
            for ig in g[:]:
                if self.__rules.checkPossibleMove(it, ig):
                    if inf_State: print('-----------------')
                    if inf_State: print('Prev:', currentCopy.getTower(), '---', currentCopy.getGround())
                    currentCopyToExpand = copy.deepcopy(currentCopy)
                    if 0 in ig: ig.remove(0)
                    if 0 in it: it.remove(0)
                    if 0 in ig: ig.remove(0)
                    if 0 in it: it.remove(0)
                    if self.__rules.calculateWeight(it) == Chest:
                        currentCopyToExpand.__ground.append(it[0])
                        currentCopyToExpand.__tower.remove(it[0])
                    else:
                        for i in ig:
                            currentCopyToExpand.__tower.append(i)
                            currentCopyToExpand.__ground.remove(i)
                        for i in it:
                            currentCopyToExpand.__tower.remove(i)
                            currentCopyToExpand.__ground.append(i)
                    currentCopyToExpand.increaseLevel()
                    currentCopyToExpand.__prevNode = self
                    expanded.append(currentCopyToExpand)
                    if inf_State:
                        print('After: Level: ', currentCopyToExpand.getLevel(), ' - ', currentCopyToExpand.getTower(),
                              '---', currentCopyToExpand.getGround())
        return expanded

    def getTuples(self, l):
        '''Return list of two-item (tuple) combinations of elements from given list L in ,
        and also adds combination of elements with zero element, f.e. [1,2] -> [[0,1],[1,2],[2,0]].
        Used for putting combinations of elements from ground or tower into basket.'''
        tuples = []
        if len(l) == 0:
            return [[0, 0]]
        for i in range(0, len(l)):
            tuples.append([0, l[i]])
        for i in range(0, len(l)):
            for x in range(i + 1, len(l)):
                tuples.append([l[i], l[x]])
        return tuples
# ----------


class Game:
    times = 0
    openStates = []
    closedStates = []
    initial = State([Queen, King, Chest, Prince, ], [])

    def __init__(self):
        self.openStates.append(self.initial)

    def checkFinalState(self, state):
        '''Checks if given state is wanted as final state.'''
        self.times += 1  # just for getting info about how many states are explored with individual algorithms
        x = state.getGround()
        if King in x and Queen in x and Prince in x and Chest in x and len(state.getTower()) == 0:
            return True
        return False

    def parseWeight(self, lis):
        '''Return list of strings of constant names'''
        r = []
        for l in lis:
            if l == King: r.append('King')
            if l == Queen: r.append('Queen')
            if l == Prince: r.append('Prince')
            if l == Chest: r.append('Chest')
        return r

    def victory(self, state):
        '''Print info about successfully found state,
        with inf_Traceback = True also prints of shortest path from initial to final state.'''
        print('\nFinal state found at level:', state.getLevel())
        print("Expanded: ", self.times)
        if inf_Traceback:
            print('Traceback: ')
            s = state
            while s.getPrevious() is not None:
                print("========")
                print('Level: ', s.getLevel())
                print('F(i): ', s.getF())
                print('Ground: ', self.parseWeight(s.getGround()))
                print('Tower: ', self.parseWeight(s.getTower()))
                s = s.getPrevious()
            print('========')
            print('Level: ', s.getLevel())
            print('F(i): ', s.getF())
            print('Ground: ', self.parseWeight(s.getGround()))
            print('Tower: ', self.parseWeight(s.getTower()))

    def checkStateInList(self, what, where):
        '''Checks if given state what is present in list of states where.'''
        if len(where) == 0:
            return False
        tower = what.getTower()
        ground = what.getGround()
        for i in where:
            wTower = i.getTower()
            wGround = i.getGround()
            if (len(tower) != len(wTower)) or (len(ground) != len(wGround)):
                return False
            for t in tower:
                if t not in wTower:
                    return False
            for g in ground:
                if g not in wGround:
                    return False
        return True

    def searchWidth(self):
        '''Implementation of state-space searching using Width-first search.'''
        print('Starting Breadth-first search')
        self.openStates.append(self.initial)
        if self.checkFinalState(self.initial):
            self.victory(self.initial)
            return
        while len(self.openStates) != 0:
            i = self.openStates.pop(0)
            if self.checkFinalState(i):
                self.victory(i)
                return
            self.closedStates.append(i)
            successors = i.expandState()
            if len(successors) == 0:
                print('No successors at this level: ', i.getLevel())
            for x in successors:
                if not self.checkStateInList(x, self.openStates) and not self.checkStateInList(x, self.closedStates):
                    self.openStates.append(x)
        assert len(self.openStates) == 0
        print('Solution Does not exist')

    def searchDepth(self):
        '''Implementation of state-space searching using Depth-first search.'''
        print('Starting Depth-first search')
        self.openStates.append(self.initial)
        if self.checkFinalState(self.initial):
            self.victory(self.initial)
            return
        while len(self.openStates) != 0:
            i = self.openStates.pop(0)
            if self.checkFinalState(i):
                self.victory(i)
                return
            self.closedStates.append(i)
            successors = i.expandState()
            if len(successors) == 0:
                print('No successors at this level: ', i.getLevel())
            for x in successors:
                if not self.checkStateInList(x, self.openStates) and not self.checkStateInList(x, self.closedStates):
                    self.openStates.insert(0, x)
        assert len(self.openStates) == 0
        print('Solution Does not exist')

    def searchInformed(self):
        '''Implementation of state-space searching using A* algorithm search.'''
        print('Starting search with A')
        self.openStates.append(self.initial)
        if Game.checkFinalState(self, self.initial):
            self.victory(self.initial)
            return
        while len(self.openStates) != 0:
            smallest = 0  # take State with smallest f(i) from openStates
            pos = 0
            for s in self.openStates:
                if s.getF() <= smallest:
                    smallest = s.getF()
                    pos = self.openStates.index(s)
            i = self.openStates.pop(pos)
            if self.checkFinalState(i):
                self.victory(i)
                return
            self.closedStates.append(i)
            successors = i.expandState()
            if len(successors) == 0:
                print('No successors at this level: ', i.getLevel())
            for j in successors:
                if not self.checkStateInList(j, self.openStates) and not self.checkStateInList(j, self.closedStates):
                    self.openStates.insert(0, j)
                else:
                    if j.getF() > i.getF():
                        j.setLevel(i.getLevel()+1)
                        j.setPrevious(i)
                        self.openStates.append(j)

        assert len(self.openStates) == 0
        print('Solution Does not exist')

if __name__ == '__main__':
    d = ''
    print('---Royal family on the run---')

    d = input('Want info about processing states?(y/n): ')
    if d in ['n', 'N', 'no', 'No', 'NO']:
        inf_State = False
    d = input('Want info about traceback? (y/n): ')
    if d in ['n', 'N', 'no', 'No', 'NO']:
        inf_Traceback = False

    print('Which algorithm:')
    print('D: Blind Depth Search')
    print('W: Blind Width Search')
    print('I: A* Informed Search')
    d = input('Input: ')
    if d not in ['W', 'D', 'I', 'w', 'd', 'i']:
        print('Unknown algorithm, aborting.')
        exit(1)

    g = Game()
    if d == 'D': g.searchDepth()
    if d == 'W': g.searchWidth()
    if d == 'I': g.searchInformed()
