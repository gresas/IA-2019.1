class arvore():
	raiz = None

class ramos():
	estado = None
	ramoPai = None
	ramosFilhos = []
	
class estado():
	mesa = None
	numJogador = -1
	visitas = 0
	pontuacaoVitoria = 0
	
	def geraEstadosPossiveis():
		return []
	
	def realizaMovimentoAleatorio():
		return None

class UCT():
	def uctValue(visitasTotais,PontVitoriaRamo, visitaRamo):
		if(visitaRamo == 0):
			return 999999999
		return (PontVitoriaRamo/visitaRamo)+ 1.41*Math.sqrt(Math.log(visitasTotais)/visitaRamo)
		
	def achaMelhorRamo(ramo):
		maximo = -999999999
		ramoRetorno = None
		visitasParente = ramo.estado.visitas
		for r in ramo.ramosFilhos:
			if(maximo<uctValue(visitasParente, r.estado.pontuacaoVitoria, r.estado.visitas)):
				maximo = uctValue(visitasParente, r.estado.pontuacaoVitoria, r.estado.visitas)
				ramoRetorno = r
		return ramoRetorno


class buscaMCTS():
	PONTUACAO_VITORIA = 10
	level = 0
	oponente = None
	
	def selecionaRamoPromisor(ramo):
		nodoRetorno = ramo
		for n in ramo.ramosFilhos:
			nodoRetorno = UCT.achaMelhorRamo(nodoRetorno)
		return nodoRetorno
	
	def expandirRamo(ramo):
		estadosPossiveis = ramo.estado.geraEstadosPossiveis()
		for e in estadosPossiveis:
			novoRamo = new ramos(e)
			novoRamo.ramoPai = ramo
			novoRamo.estado.numJogador=3-ramo.estado.numJogador
			ramo.ramosFilhos.add(novoRamo)
	
	def propagarInterno(ramoExplorar, numJogador):
		ramoTemp = ramoExplorar
		while(ramoTemp!=None):
			ramoTemp.estado.visitas+=1
			if(ramoTemp.estado.numJogador == numJogador):
				ramoTemp.estado.pontuacaoVitoria+=1
			ramoTemp = ramoTemp.ramoPai
			
	def simularResultadoJogo(ramo):
		ramoTemp = new ramos()
		estadoTemp = ramoTemp.estado
		estadoDaMesa = checarEstadoMesa(estadoTemp.mesa)
		if(estadoDaMesa==oponente):
			ramoTemp.ramoPai.estado.pontuacaoVitoria=-999999999
			return estadoDaMesa
		else:
			estadoTemp.numJogador = 3 - estadoTemp.numJogador
			estadoTemp.realizaMovimentoAleatorio()
			estadoDaMesa = checarEstadoMesa(estadoTemp.mesa)
		return estadoDaMesa
		
	
	def achaNovoMovimento(mesa, numJogador):
		oponente = 3-numJogador
		tree = new arvore()
		ramoRaiz = tree.raiz
		ramoRaiz.estado.mesa = mesa
		ramoRaiz.estado.numJogador = oponente
		while(True):
			ramoPromisor = selecionaRamoPromisor(ramoRaiz)
			expandirRamo(ramoPromisor)
			ramoExplorar = ramoPromisor
			if(ramoPromisor.ramosFilhos.length >0):
				ramoExplorar=ramoPromisor.filhoAleatorio()
			resultadoJogo = simularResultadoJogo(ramoExplorar)
			propagarInterno(ramoExplorar,resultadoJogo)
		vencedor = ramoRaiz.filhoComMaiorPontuacao
		tree.defineRaiz(vencedor)
		return vencedor.estado.mesa
	
	
		