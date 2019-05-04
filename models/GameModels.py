import PieceModels as pm
import ..utils.util as u

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
    self.heap = None
    self.player_list = None
    self.num_pieces_per_player = 7

    def buildTable(self, players):
        self.player_list = Players()
        self.player_list.players = players
        
        self.heap = Heap()
        initGameBuild(self.player_list, self.heap)

    def initGameBuild(self, players, heap):
        pieces = GroupPieces()
    
        for i in range(num_pieces_per_player):
            for j in range(i, num_pieces_per_player):
                p = Piece(i, j)
                pieces.appendPiece(p)
        heap.setHeap(pieces)
        for p in players.getPlayers():
            for i in range(num_pieces_per_player):
                p.buy(heap)

    
    




        '''
        self.matriz = MatrizMesa(self.len_mesa_matriz) 
    
    def turno(self):
        matriz_bkp = self.matriz
        monte_bkp = self.monte
        self.jogadores.retornaJogador(0).tempoDeRodada(self.matriz, self.monte)
        if(self.matriz != matriz_bkp):
            if(self.matriz.verificaJogada()):
                self.jogadores.moveJogadorProFinal(self.jogadores.retornaJogador(0))
                return
            else:
                print('Sua jogada foi inválida, retornando jogo ao estado anterior...')
                self.matriz = matriz_bkp
        if(monte_bkp == self.monte):
            self.monte = self.jogadores.retornaJogador(0).compraPecaMonte(self.monte)
        self.jogadores.moveJogadorProFinal(self.jogadores.retornaJogador(0))
        # Fim do turno
        self.turnos += 1
    

class MatrizMesa:
    def __init__(self, len_mesa_matriz):
        self.matriz_mesa = [[-1 for i in range(len_mesa_matriz)] for k in range(len_mesa_matriz)]

    def verificaJogada():
        # Aqui onde é feita a verificação da jogada
        return True

'''