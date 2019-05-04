import random,math
from copy import deepcopy
class board():
    DEFAULT_BOARD_SIZE = 3
    boardValues = [[0,0,0],[0,0,0],[0,0,0]]
    IN_PROGRESS = -1
    DRAW = 0
    P1 = 1
    P2 = 2
    totalMoves=0
    def __init__(self):
            self.boardValues = [[0,0,0],[0,0,0],[0,0,0]]
            
     
    def performMove(self,player, p):
        self.totalMoves+=1
        self.boardValues[p[0]][p[1]] = player
 
    def checkStatus(self):
        boardSize = self.boardValues.__len__()
        maxIndex = boardSize - 1
        diag1 = [0,0,0]
        diag2 = [0,0,0]
        
        for i in range(0,boardSize):
            row = self.boardValues[i]
            col = [0,0,0]
            for j in range(0,boardSize):
                    col[j] = self.boardValues[j][i]
    
            checkRowForWin = self.checkForWin(row)
            if(checkRowForWin!=0):
                return checkRowForWin
            
            checkColForWin = self.checkForWin(col)
            if(checkColForWin!=0):
                return checkColForWin
            
            diag1[i] = self.boardValues[i][i]
            diag2[i] = self.boardValues[maxIndex - i][i]
        

        checkDia1gForWin = self.checkForWin(diag1)
        if(checkDia1gForWin!=0):
            return checkDia1gForWin
        
        checkDiag2ForWin = self.checkForWin(diag2)
        if(checkDiag2ForWin!=0):
            return checkDiag2ForWin
        
        if (self.getEmptyPositions().__len__() > 0):
            return self.IN_PROGRESS
        else:
            return self.DRAW
    

    def checkForWin(self,row):
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
 
    def getEmptyPositions(self):
        size = self.boardValues.__len__()
        emptyPositions = []
        for i in range(0,size):
            for j in range(0, size):
                if (self.boardValues[i][j] == 0):
                    emptyPositions.append([i,j]);
        return emptyPositions;

        
class estado():
        mesa = board()
        numJogador = -1
        visitas = 0
        pontuacaoVitoria = 0
        def __init__(self):
                self.mesa = board()
                self.numJogador = -1
                self.visitas=0
                self.pontuacaoVitoria = 0

        def geraEstadosPossiveis(self):
                possibleStates = []
                availablePositions = self.mesa.getEmptyPositions()
                for p in availablePositions:
                        newState = estado()
                        newState.mesa = deepcopy(self.mesa)
                        newState.numJogador = 3 - self.numJogador
                        newState.mesa.performMove(newState.numJogador, p)
                        possibleStates.append(newState)
                
                return possibleStates;


class ramos():
	estado = estado()
	ramoPai = None
	ramosFilhos = []

	def __init__(self):
		self.estado = estado()
		self.ramoPai = None
		self.ramosFilhos = []
	
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

class UCT():
	def uctValue(visitasTotais,PontVitoriaRamo, visitaRamo):
		if(visitaRamo == 0 or visitasTotais==0):
			return 999999999
		return (PontVitoriaRamo/visitaRamo)+ 1.41*((math.log(visitasTotais)/visitaRamo)**(1/2))
		
	def achaMelhorRamo(ramo):
		maximo = -999999999
		ramoRetorno = None
		visitasParente = ramo.estado.visitas
		for r in ramo.ramosFilhos:
			if(maximo<UCT.uctValue(visitasParente, r.estado.pontuacaoVitoria, r.estado.visitas)):
				maximo = UCT.uctValue(visitasParente, r.estado.pontuacaoVitoria, r.estado.visitas)
				ramoRetorno = r
		return ramoRetorno


class buscaMCTS():
	PONTUACAO_VITORIA = 10
	level = 0
	oponente = None
	def __init__(self):
		self.oponente = None
	
	def selecionaRamoPromisor(ramo):
		nodoRetorno = ramo
		while(nodoRetorno.ramosFilhos.__len__()>0):
			nodoRetorno = UCT.achaMelhorRamo(nodoRetorno)
		return nodoRetorno
	
	def expandirRamo(ramo):
		estadosPossiveis = ramo.estado.geraEstadosPossiveis()
		for e in estadosPossiveis:
			novoRamo = ramos()
			novoRamo.estado = e
			novoRamo.ramoPai = ramo
			novoRamo.estado.numJogador=3-ramo.estado.numJogador
			ramo.ramosFilhos.append(novoRamo)
	
	def propagarInterno(ramoExplorar, numJogador):
		ramoTemp = ramoExplorar
		while(ramoTemp!=None):
			ramoTemp.estado.visitas+=1
			if(ramoTemp.estado.numJogador == numJogador):
				ramoTemp.estado.pontuacaoVitoria+=1
			ramoTemp = ramoTemp.ramoPai
			
	def simularResultadoJogo(ramo):
		ramoTemp = deepcopy(ramo)
		estadoTemp = deepcopy(ramoTemp.estado)
		estadoDaMesa = estadoTemp.mesa.checkStatus()
		if(estadoDaMesa==3-ramoTemp.estado.numJogador and ramoTemp.ramoPai!=None):
			ramoTemp.ramoPai.estado.pontuacaoVitoria=-999999999
			return estadoDaMesa
		while(estadoDaMesa == board.IN_PROGRESS):
			estadoTemp.numJogador = 3 - estadoTemp.numJogador
			escolhas = estadoTemp.mesa.getEmptyPositions()
			if(escolhas!=[]):estadoTemp.mesa.performMove(estadoTemp.numJogador,random.choice(escolhas))
			estadoDaMesa = estadoTemp.mesa.checkStatus()
		return estadoDaMesa
		
	
	def achaNovoMovimento(mesa, numJogador):
		oponente = 3-numJogador
		tree= None
		tree = arvore()
		ramoRaiz = tree.raiz
		ramoRaiz.estado.mesa = mesa
		ramoRaiz.estado.numJogador = oponente
		for i in range(0,4):
			ramoPromisor = buscaMCTS.selecionaRamoPromisor(ramoRaiz)
			#print(ramo)
			if(ramoPromisor.estado.mesa.checkStatus()==board.IN_PROGRESS):
			    buscaMCTS.expandirRamo(ramoPromisor)
			#print(ramoRaiz.ramosFilhos.__len__())

			ramoExplorar = ramoPromisor
			#print(ramoRaiz.ramosFilhos.__len__())

			if(ramoPromisor.ramosFilhos.__len__()>0):
				ramoExplorar=random.choice(ramoPromisor.ramosFilhos)
			resultadoJogo = buscaMCTS.simularResultadoJogo(ramoExplorar)
			print(ramoExplorar.estado.mesa.boardValues)
			#print(resultadoJogo)
			buscaMCTS.propagarInterno(ramoExplorar,resultadoJogo)
			#print(ramoRaiz.ramosFilhos.__len__())
		vencedor = ramoRaiz.filhoComMaiorPontuacao()
		#print(ramoRaiz.estado.mesa.boardValues)
		#print(vencedor.estado.mesa.boardValues)
		#print(";;;;;;;;;;;;;;;;;;;;;;;;;")
		tree.raiz = vencedor
		return vencedor.estado.mesa


def givenEmptyBoard_whenSimulateInterAIPlay_thenGameDraw(b):
        boardT = b
        player = board.P1;
        totalMoves = board.DEFAULT_BOARD_SIZE * board.DEFAULT_BOARD_SIZE;
        for i in range(0, totalMoves):
                print(boardT.boardValues)
                boardT = buscaMCTS.achaNovoMovimento(boardT, player)
                if (boardT.checkStatus() != -1):
                        break 
                player = 3 - player;
                print(boardT.boardValues)
                print("////////")
    
        winStatus = boardT.checkStatus();
        print("Vitoria de:"+str(winStatus))
        print(boardT.boardValues[0])
        print(boardT.boardValues[1])
        print(boardT.boardValues[2])

        
givenEmptyBoard_whenSimulateInterAIPlay_thenGameDraw(board())

