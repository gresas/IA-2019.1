from .PieceModels  import *

class Monte:

    def __init__(self):
        # no inicio, o monte contém todas as peças do jogo
        self.montePecas = Pecas()

    def embaralhaMonte(self):
        self.montePecas.embaralhaPecas()

    def atribuiPecasMonte(self, pecas):
        self.montePecas = pecas

    def contaPecasMonte(self):
        return self.montePecas.contaPecas()

    def removePecaAleatoria(self):
        p = self.montePecas.removePecaAleatoria()
        return self.montePecas.removePeca(p)

    def retornaMonte(self):
        return self.montePecas.retornaPecas()


class Suporte:

    def __init__(self):
        self.listaPecas = Pecas()

    def compraPeca(self, monte):
        p = monte.removePecaAleatoria()
        self.listaPecas.adcionaPeca(p)

    def atribuiPecasSuporte(self, pecas):
        self.listaPecas = pecas

    def removePeca(self, p):
        return self.listaPecas.removePeca(p)

    def contaPecasSuporte(self):
        return self.listaPecas.contaPecas()

    def retornaSuporte(self):
        return self.listaPecas.retornaPecas()

    def somaValoresSuporte(self):
        return self.listaPecas.somaValoresPecas()

    # Need to implement
    def ordenaPecas(self, modo):
        self.listaPecas.ordenaPecas(modo)

        
class Mesa:
    turnos = 0
    len_mesa_matriz = 11

    def __init__(self, jogadores, monte):
        self.jogadores = jogadores
        self.monte = monte
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