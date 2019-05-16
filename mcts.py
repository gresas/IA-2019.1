# -*- coding: utf-8 -*-
import random,math
from copy import deepcopy
import PieceModels as pm
from PlayerModel import *
from PieceModels import *
from GameModels import *
import util as u
import time

        
class Table():
    heap = None
    player_list = None
    num_pieces_per_player = 7
    game_table = None
    
    #MCTS
    DEFAULT_BOARD_SIZE = 3
    IN_PROGRESS = -1
    DRAW = 0
    P1 = 1
    P2 = 2
    totalMoves=0
    
    def __init__(self):
        self.player_list = Players()
        self.pecasJgIA = -1
        
    #serve para checar condições de vitoria ou empate 
    def checaEstadoMesa(self):
        for player in self.player_list.getPlayers():
        #print(player.hand.getHand().lenGroupPieces())
            if(not player.hand.getHand().lenGroupPieces()>0):
                return True
        return self.IN_PROGRESS
    
 
     #função responsável para encontrar todos lugares jogaveis PRECISA ALTERAR
    def geraJogadas(self, p):
        if(p<self.player_list.getPlayers().__len__()):
            return self.player_list.getPlayerFromIndex(p).hand.getHand().possiveisJogadas(self.game_table)
        return []

    def buildTable(self, players):
        self.player_list = Players()
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

    def turn(self, player, round_n):
        if(player.isValidHand(self.game_table)):
            pop_piece = None
            if(self.game_table):
                print("=======================================================")
                print("Game Table:")
                self.printGameTable()
            else:
                print('Round %s\n'%round_n)
            if(player.IA):
                print('Player of the turn (IA): %s'%player.nick)
                print('Here is your hand: \n')
                player.printHand()
                start = time.time()
                melhor = buscaMINMAX.minimax(buscaMINMAX(),7,1,self)
                print("-------Resultado-------")
                print(melhor)
                print("-----------------------")
                piece_position = melhor[0]
                end = time.time()
                print("Tempo de execução de IA (8 Verificações): "+str(end - start))
                #print(piece_position)
        #player.printHand()
                pop_piece = player.checkPlay(self.game_table, piece_position)
        #player.printHand()
        #self.printGameTable()
            else:
                while(not pop_piece):
                    piece_position = u.turnMenu(player)
                    pop_piece = player.checkPlay(self.game_table, piece_position)
                    if(pop_piece): break
                    print('\nJogada inválida, tente novamente...\n')
            self.insertTable(pop_piece)
            print("=======================================================")
        #print("Aqui?")
        else:
            print('Não há jogadas possiveis, comprando uma peça... ',player.nick)
            p_buy = player.buy(self.heap)
            if(not p_buy):
                print('Peças indisponiveis.. passando a vez')
                return False
            print('Peça adquirida: |%s|%s|\n\n'%p_buy)
            self.turn(player, round_n)

    #print("Aqui?")
        return True

    def printGameTable(self):
        print_obj = [': |%s|%s| :'%(t) for t in self.game_table]
        print("".join(print_obj)+'\n')

    def insertTable(self, piece):
        self.totalMoves+=1
        if(not self.game_table):
            self.game_table.insert(0, (piece.left_value, piece.right_value))
        else:
            first, last = u.parseGameTable(self.game_table)
            if(piece.left_value == first):
                self.game_table.insert(0, (piece.right_value, piece.left_value))
            elif(piece.right_value == first):
                self.game_table.insert(0, (piece.left_value, piece.right_value))
            elif(piece.left_value == last):
                self.game_table.insert(len(self.game_table), (piece.left_value, piece.right_value))
            elif(piece.right_value == last):
                self.game_table.insert(len(self.game_table), (piece.right_value, piece.left_value))
        
    def clearTable(self):
        self.heap = Heap()
        self.game_table = list()
        map(lambda p: p.clearHand(), self.player_list.getPlayers())
        self.initGameBuild(self.player_list, self.heap)
#É o tabuleiro do jogo, dependendo do jogo, é a parte que mais necessita alterar quando muda o jogo
#IMPORTANTE APENAS mesaClasse PRECISA MUDAR, O RESTO NÂO UTILIZA NADA DISSO
class mesa():
    DEFAULT_BOARD_SIZE = 3
    mesaClasseValues = [[0,0,0],[0,0,0],[0,0,0]]
    IN_PROGRESS = -1
    DRAW = 0
    P1 = 1
    P2 = 2
    totalMoves=0
    #init serve para instancia o mesaClasseValues para cada objeto ao inves de um global
    def __init__(self):
        self.mesaClasseValues = [[0,0,0],[0,0,0],[0,0,0]]
            
    #funcao serve para realizar movimento adicionando o valor do jogando no tabuleiro PRECISA ALTERAR
    def realizaMovimento(self,player, p):
        self.totalMoves+=1
        self.mesaClasseValues[p[0]][p[1]] = player
        
    #serve para checar condições de vitoria ou empate para jogo da velha PRECISA ALTERAR
    def checaEstadoMesa(self):
        mesaClasseSize = self.mesaClasseValues.__len__()
        maxIndex = mesaClasseSize - 1
        diag1 = [0,0,0]
        diag2 = [0,0,0]
        
        for i in range(0,mesaClasseSize):
            row = self.mesaClasseValues[i]
            col = [0,0,0]
            for j in range(0,mesaClasseSize):
                col[j] = self.mesaClasseValues[j][i]
    
            checkRowForWin = self.checaVitoria(row)
            if(checkRowForWin!=0):
                return checkRowForWin
            
            checkColForWin = self.checaVitoria(col)
            if(checkColForWin!=0):
                return checkColForWin
            
            diag1[i] = self.mesaClasseValues[i][i]
            diag2[i] = self.mesaClasseValues[maxIndex - i][i]
        

        checkDia1gForWin = self.checaVitoria(diag1)
        if(checkDia1gForWin!=0):
            return checkDia1gForWin
        
        checkDiag2ForWin = self.checaVitoria(diag2)
        if(checkDiag2ForWin!=0):
            return checkDiag2ForWin
        
        if (self.geraJogadas().__len__() > 0):
            return self.IN_PROGRESS
        else:
            return self.DRAW
    
    #checa vitoria para jogo da velha PRECISA MUDAR
    def checaVitoria(self,row):
        isEqual = True
        size = row.__len__()
        previous = row[0]
        for i in range(0,size):
            if (previous != row[i]):
                isEqual = False
                break
            previous = row[i]
        
        if(isEqual):
            return previous
        else:
            return 0
     #função responsável para encontrar todos lugares jogaveis PRECISA ALTERAR
    def geraJogadas2(self):
        size = self.mesaClasseValues.__len__()
        emptyPositions = []
        for i in range(0,size):
            for j in range(0, size):
                if (self.mesaClasseValues[i][j] == 0):
                    emptyPositions.append([i,j]);
        return emptyPositions;

        
class estado():
        mesa = Table()
        numJogador = -1
        visitas = 0
        pontuacaoVitoria = 0
        #init serve para instancia o mesaClasseValues para cada objeto ao inves de um global
        def __init__(self):
            self.mesa = Table()
            self.numJogador = -1
            self.visitas=0
            self.pontuacaoVitoria = 0
            self.posicaoPeca = -1
        #gera todos os resultado de estado da mesa possiveis com base nos lugares que pode jogar, UTILIZAR PARA DEFINIR JOGADAS COM BASE NA MÃO DE CADA JOGADOR
        def geraEstadosPossiveis(self):
            possibleStates = []
            availablePositions = self.mesa.geraJogadas(self.numJogador-1)
        #print("NumJ"+str(self.numJogador))
            for p in availablePositions:
                newState = estado()
                newState.mesa = deepcopy(self.mesa)
                newState.numJogador = 3 - self.numJogador
                newState.mesa.insertTable(p[1])
                newState.posicaoPeca = p[0]
        #    print(p[0])
        #    print("AQUI")
                if(p[0]<self.mesa.player_list.players[self.numJogador-1].hand.len()):self.mesa.player_list.players[self.numJogador-1].checkPlay(self.mesa.game_table, p[0])
                possibleStates.append(newState)
            return possibleStates;



class ramos():
    estado = estado()
    ramoPai = None
    ramosFilhos = []

        #init serve para instancia o mesaClasseValues para cada objeto ao inves de um global
    def __init__(self):
        self.estado = estado()
        self.ramoPai = None
        self.ramosFilhos = []

    #função geral que verifica qual filho tem a melhor pontuação e é o ganhador
    def filhoComMaiorPontuacao(ramo):
        maximo = -999999999
        ramoRetorno = ramo.ramosFilhos[0]
        visitasParente = ramo.estado.visitas
        for r in ramo.ramosFilhos:
            if(r.estado.visitas>=ramoRetorno.estado.visitas):
                ramoRetorno = r
            #print(r.estado.visitas)
        return ramoRetorno

class arvore():
    raiz = ramos()

    def __init__(self):
        self.raiz = ramos()


class buscaMINMAX():
    PONTUACAO_VITORIA = 10
    level = 0
    oponente = None
    def __init__(self):
        self.oponente = None

    #funcao que avalia o estado do jogo com base no tamanho das mãos
    def avaliar(self,estado):
        if(estado.mesa.player_list.players[0].hand.len()==0 and estado.mesa.player_list.players[1].hand.len()!=0):
            print("teste")
            return +10        
        elif(estado.mesa.player_list.players[0].hand.len()!=0 and estado.mesa.player_list.players[1].hand.len()==0):
            print("teste")
            return -10
        elif(estado.mesa.player_list.players[0].hand.len()>estado.mesa.player_list.players[1].hand.len()):
            return +1
        elif(estado.mesa.player_list.players[0].hand.len()<estado.mesa.player_list.players[1].hand.len()):
            return -1
        else:
            return 0

    def minimax(self,profundidade,numJogador,mesa):
        est = estado()
        est.mesa=deepcopy(mesa)
        est.numJogador=numJogador+1
        #inicia o melhor com informacoes limpas
        if(numJogador==1):
            melhor = [-1,-11111]
        else:
            melhor = [-1,11111]
        #se acabou a profundidade ou alguem ganhou o jogo, para de pesquisar

        if(profundidade==0 or est.mesa.player_list.players[0].hand.len()==0 or est.mesa.player_list.players[1].hand.len()==0):
            #print(buscaMINMAX().avaliar(est))
            return [-1,buscaMINMAX().avaliar(est)]
        #verifico para cada jogada possivel, qual a melhor jogada e repito o minimax
        jogadas = est.geraEstadosPossiveis()

        #compra cartas enquanto precisar ate acabar as cartas ou jogadas        
        p_buy=True
        while jogadas==[] and p_buy:
            p_buy = est.mesa.player_list.players[numJogador].buy(est.mesa.heap)
            jogadas = est.geraEstadosPossiveis()

        for jogada in jogadas:
            retorno = buscaMINMAX().minimax(profundidade-1,1-numJogador,jogada.mesa)
            #eh IA     
            #print(melhor)			
            if(numJogador==1):
                if(retorno[1]>melhor[1]):
                    melhor = [jogada.posicaoPeca,retorno[1]]
            else:
                if(retorno[1]<melhor[1]):
                    melhor = [jogada.posicaoPeca,retorno[1]]    
        
        #print("MAO 1:" +str(est.mesa.player_list.players[0].hand.len()))
        #print("MAO 2:" +str(est.mesa.player_list.players[1].hand.len()))
        #print(melhor)        
        return melhor
            

    #printa a arvore, comentando só pra deixar estético
    def printaArvore(self,textoInit,ramo):
        print(textoInit+"NumJ="+str(ramo.estado.numJogador)+" Visitas="+str(ramo.estado.visitas)+" Pontuacao="+str(ramo.estado.pontuacaoVitoria)+" EspacoMao:"+str(ramo.estado.posicaoPeca))
        for p in ramo.ramosFilhos:
            buscaMCTS.printaArvore(buscaMCTS(),textoInit+"    ",p)
        return None
    


        

