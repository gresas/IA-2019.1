from . import PieceModels as pm
from . import PlayerModel as pp
from .utils import util as u

class Heap:

    def __init__(self):
        self.heap_list = pm.GroupPieces()

    def getHeap(self):
        return self.heap_list

    def setHeap(self, pieces):
        self.heap_list = pieces

    def shuffleHeap(self):
        self.heap_list.shuffle()

    def len(self):
        return self.heap_list.lenGroupPieces()


class HandSupport:

    def __init__(self):
        self.piece_list = pm.GroupPieces()

    def setHand(self, pieces):
        self.piece_list = pieces

    def getHand(self):
        return self.piece_list

    def pop(self, p):
        return self.piece_list.popPiece(p)

    def len(self):
        return self.piece_list.lenGroupPieces()

    def sumValue(self):
        return self.piece_list.getSumValue()

    def maxValue(self):
        return self.piece_list.getMaxValue()

        
class Table:
    heap = None
    player_list = None
    num_pieces_per_player = 7
    game_table = None

    def buildTable(self, players):
        self.player_list = pp.Players()
        self.player_list.players = players
        self.heap = Heap()
        self.game_table = list()
        self.initGameBuild(self.player_list, self.heap)

    def initGameBuild(self, players, heap):
        pieces = pm.GroupPieces()
        for i in range(self.num_pieces_per_player):
            for j in range(i, self.num_pieces_per_player):
                p = pm.Piece(i, j)
                pieces.appendPiece(p)
        heap.setHeap(pieces)
        for p in players.getPlayers():
            for i in range(self.num_pieces_per_player):
                p.buy(heap)

    def turn(self, player):
        #print('JOGADOR %s'%player.nick)
        #player.printHand()
        if(player.isValidHand(self.game_table)):
            pop_piece = None
            print("Game Table:")
            self.printGameTable()
            while(not pop_piece):
                piece_position = u.turnMenu(player)
                pop_piece = player.checkPlay(self.game_table, piece_position)
                if(pop_piece): break
                print('Jogada inválida, tente novamente...')
            self.insertTable(pop_piece)
        else:
            print('Não há jogadas possiveis, comprando uma peça...')
            print('Peça adquirida: |%s|%s|\n\n'%player.buy(self.heap))
            self.turn(player)
        
    def printGameTable(self):
        [print('|%s|%s|'%(t)) for t in self.game_table]
        print('\n')

    def insertTable(self, piece):
        if(not self.game_table):
            self.game_table.insert(0, (piece.left_value, piece.right_value))
        else:
            first, last = u.parseGameTable(self.game_table)
            if(piece.left_value == first):
                self.game_table.insert(0, (piece.right_value, piece.left_value))
            elif(piece.left_value == last):
                self.game_table.insert(0, (piece.left_value, piece.right_value))
            elif(piece.right_value == first):
                self.game_table.insert(len(self.game_table), (piece.left_value, piece.right_value))
            elif(piece.right_value == last):
                self.game_table.insert(len(self.game_table), (piece.right_value, piece.left_value))
        