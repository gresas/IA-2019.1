import random,math
from copy import deepcopy

#É o tabuleiro do jogo, dependendo do jogo, é a parte que mais necessita alterar quando muda o jogo
#IMPORTANTE APENAS mesaClasse PRECISA MUDAR, O RESTO NÂO UTILIZA NADA DISSO
class mesaClasse():
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
    def geraJogadas(self):
        size = self.mesaClasseValues.__len__()
        emptyPositions = []
        for i in range(0,size):
            for j in range(0, size):
                if (self.mesaClasseValues[i][j] == 0):
                    emptyPositions.append([i,j]);
        return emptyPositions;

        
class estado():
        mesa = mesaClasse()
        numJogador = -1
        visitas = 0
        pontuacaoVitoria = 0
        #init serve para instancia o mesaClasseValues para cada objeto ao inves de um global
        def __init__(self):
                self.mesa = mesaClasse()
                self.numJogador = -1
                self.visitas=0
                self.pontuacaoVitoria = 0
        #gera todos os resultado de estado da mesa possiveis com base nos lugares que pode jogar, UTILIZAR PARA DEFINIR JOGADAS COM BASE NA MÃO DE CADA JOGADOR
        def geraEstadosPossiveis(self):
                possibleStates = []
                availablePositions = self.mesa.geraJogadas()
                for p in availablePositions:
                        newState = estado()
                        newState.mesa = deepcopy(self.mesa)
                        newState.numJogador = 3 - self.numJogador
                        newState.mesa.realizaMovimento(newState.numJogador, p)
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

class UCT():
        #com base no estado do ramo, gera a pontuação uct, que é usado para selecionar qual ramo será o melhor
	def uctValue(visitasTotais,PontVitoriaRamo, visitaRamo):
		if(visitaRamo == 0 or visitasTotais==0):
			return 999999999
		return (PontVitoriaRamo/visitaRamo)+ 1.41*((math.log(visitasTotais)/visitaRamo)**(1/2))
	    
	#verifica os uct de cada ramo para selecionar o melhor	
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

	#printa a arvore, comentando só pra deixar estético
	def printaArvore(textoInit,ramo):
		print(textoInit+"NumJ="+str(ramo.estado.numJogador)+" Visitas="+str(ramo.estado.visitas)+" Pontuacao="+str(ramo.estado.pontuacaoVitoria))
		for p in ramo.ramosFilhos:
		    buscaMCTS.printaArvore(textoInit+"    ",p)
		return None
	#seleciona o melhor filho por UCT, verificado cada um
	def selecionaRamoPromisor(ramo):
		nodoRetorno = ramo
		while(nodoRetorno.ramosFilhos.__len__()>0):
			nodoRetorno = UCT.achaMelhorRamo(nodoRetorno)
		return nodoRetorno
	#basicamente verifica todos os estados que podem ser gerado e a partir disso, gera os filhos do ramo
	def expandirRamo(ramo):
		estadosPossiveis = ramo.estado.geraEstadosPossiveis()
		for e in estadosPossiveis:
			novoRamo = ramos()
			novoRamo.estado = e
			novoRamo.ramoPai = ramo
			novoRamo.estado.numJogador=3-ramo.estado.numJogador
			ramo.ramosFilhos.append(novoRamo)
	#basicamente vai indo de pai a pai ajustando os pontos de vitoria e visita
	def propagarInterno(ramoExplorar, numJogador):
		ramoTemp = ramoExplorar
		while(ramoTemp!=None):
			ramoTemp.estado.visitas+=1
			if(ramoTemp.estado.numJogador == numJogador):
				ramoTemp.estado.pontuacaoVitoria+=1
			ramoTemp = ramoTemp.ramoPai

	#simula um resultado aleatoria de jogo, checando o status e vendo se alguem venceu, se não, repete uma jogada totalmente aleatoria a partir da mesa atual
	def simularResultadoJogo(ramo):
		ramoTemp = deepcopy(ramo)
		estadoTemp = deepcopy(ramoTemp.estado)
		estadoDaMesa = estadoTemp.mesa.checaEstadoMesa()
		if(estadoDaMesa==3-ramoTemp.estado.numJogador and ramoTemp.ramoPai!=None):
			ramoTemp.ramoPai.estado.pontuacaoVitoria=-999999999
			return estadoDaMesa
		while(estadoDaMesa == mesaClasse.IN_PROGRESS):
			estadoTemp.numJogador = 3 - estadoTemp.numJogador
			escolhas = estadoTemp.mesa.geraJogadas()
			if(escolhas!=[]):estadoTemp.mesa.realizaMovimento(estadoTemp.numJogador,random.choice(escolhas))
			estadoDaMesa = estadoTemp.mesa.checaEstadoMesa()
		return estadoDaMesa
		
	#função principal da ia, serve para buscar o próximo movimento dependendo do jogador e estado da mesa, ele seleciona qual filho é melhor por UCT, cria os filhos desse ramo
	#escolhe um filho aleatorio(rodada aleatoria) do ramo e simula o jogo a partir desse filho depois ajusta os valores de todos os pais
	#depois, por causa da propagação, verifica o filho da raiz com melhor pontuação
	def achaNovoMovimento(mesa, numJogador):
		oponente = 3-numJogador
		tree= None
		tree = arvore()
		ramoRaiz = tree.raiz
		ramoRaiz.estado.mesa = mesa
		ramoRaiz.estado.numJogador = oponente
		#importante, aumentar esse valor deixa a ia mais inteligente, vai deixar ela fazer mais verificações na árvore
		for i in range(0,8):
			ramoPromisor = buscaMCTS.selecionaRamoPromisor(ramoRaiz)
			if(ramoPromisor.estado.mesa.checaEstadoMesa()==mesaClasse.IN_PROGRESS):
			    buscaMCTS.expandirRamo(ramoPromisor)
			ramoExplorar = ramoPromisor
			if(ramoPromisor.ramosFilhos.__len__()>0):
				ramoExplorar=random.choice(ramoPromisor.ramosFilhos)
			resultadoJogo = buscaMCTS.simularResultadoJogo(ramoExplorar)
			buscaMCTS.propagarInterno(ramoExplorar,resultadoJogo)
		vencedor = ramoRaiz.filhoComMaiorPontuacao()
		print("Inicio da árvore")
		buscaMCTS.printaArvore("",tree.raiz)
		print("Fim da árvore")
		tree.raiz = vencedor
		return vencedor.estado.mesa


#tem que mudar um pouco tbm, mas função principal que vai jogando
def simulaJogoIA_utilizaMesaVazia(b):
        mesaClasseT = b
        player = mesaClasse.P1;
        totalMoves = mesaClasse.DEFAULT_BOARD_SIZE * mesaClasse.DEFAULT_BOARD_SIZE;
        for i in range(0, totalMoves):
                mesaClasseT = buscaMCTS.achaNovoMovimento(mesaClasseT, player)
                if (mesaClasseT.checaEstadoMesa() != -1):
                        break 
                player = 3 - player;
    
        winStatus = mesaClasseT.checaEstadoMesa();
        print("Vitoria de:"+str(winStatus))
        print(mesaClasseT.mesaClasseValues[0])
        print(mesaClasseT.mesaClasseValues[1])
        print(mesaClasseT.mesaClasseValues[2])

        
simulaJogoIA_utilizaMesaVazia(mesaClasse())

