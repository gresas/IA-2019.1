from . import GameModels as gm

class Player:
    score = 0

    def __init__(self, nickname):
        self.nick = nickname
        self.hand = gm.HandSupport()
    
    def getName(self):
        return self.nick

    def getPlayerHand(self):
        return self.hand

    def greaterPieceValue(self):
        return self.hand.maxValue()

    def setPlayerHand(self, pieces):
        self.hand.setHand(pieces)

    def setScore(self, value):
        self.score = value

    def buy(self, heap):
        p = heap.getHeap().randomChoose()
        heap.getHeap().popPiece(p)
        self.hand.getHand().appendPiece(p)
        return (p.left_value, p.right_value)

    def checkPlay(self, game_table, position):
        p = self.hand.getHand().getPieceFromIndex(position)
        if(p.isCorrect(game_table)):
            return self.hand.getHand().popIndexPiece(position)
        return False

    def isValidHand(self, table_tuple):
        return self.hand.getHand().followTheRules(table_tuple)

    def sortHand(self):
        self.hand.getHand().getGroupPieces().sort()

    def printHand(self):
        self.hand.getHand().printPieces()

    # Need to implement
    def calculaPontuacao(self):
        return True


class Players:

    def __init__(self):
        self.players = list()

    def getPlayers(self):
        return self.players

    def getPlayerPosition(self, player):
        return self.players.index(player)

    def getPlayerFromIndex(self, position):
        return self.players[position]

    def appendPlayer(self, player):
        self.players.append(player)

    def popPlayer(self, player):
        return self.players.pop(self.getPlayerPosition(player))

    def insertPlayer(self, position, player):
        return self.players.insert(position, player)

    def turnToNextPlayer(self, player):
        self.insertPlayer(len(self.players) - 1, self.popPlayer(self.players[0]))