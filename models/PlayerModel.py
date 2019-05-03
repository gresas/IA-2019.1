import GameModels as gm

class Player:
    score = 0

    def __init__(self, nickname):
        self.nick = nickname
        self.hand = gm.HandSupport()
    
    def getName(self):
        return self.nick

    def getPlayerHand(self):
        return self.hand

    def setPlayerHand(self, pieces):
        self.hand.setHand(pieces)

    def setScore(self, value):
        self.score = value

    def buy(self, heap):
        p = heap.getHeap().randomChoose()
        heap.getHeap().popPiece(p)
        self.hand.getHand().appendPiece(p)

    def sortHand(self):
        self.hand.getHand().getGroupPieces().sort()

    def tempoDeRodada(self, matriz, monte):
        op = str(input("1 - Comprar peça e pular a vez\n2 - Realizar Jogada"))
        if(op == "1"):
            self.buy(monte)
        else:
            pass
            #  Aqui que o jogador faz suas jogadas
        
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
        self.insertPlayer(len(self.players) - 1, self.popPlayer(player))