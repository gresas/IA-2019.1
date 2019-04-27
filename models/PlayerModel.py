from .GameModels import *

class Jogador:
    pontuacao = 0

    def __init__(self, apelido):
        self.apelido = apelido
        self.suporte = Suporte()

    def mostraSuporte(self):
        return self.suporte.retornaSuporte()

    def atribuiSuporte(self, pecasSuporte):
        self.suporte = pecasSuporte

    def atribuiPontuacao(self, valor):
        self.pontuacao = valor

    def compraPecaMonte(self, monte):
        self.suporte.compraPeca(monte)
        
    def somaValoresSuporte(self):
        return self.suporte.somaValoresSuporte()

    # Modo: 1 => Sequencia de cores iguais
    #       2 => Grupos de cores diferentes
    def ordenaSuporte(self, modo):
        if(modo == 1 or modo == 2):
            self.suporte.ordenaPecas(modo)

    def tempoDeRodada(self, matriz, monte):
        op = str(input("1 - Comprar peça e pular a vez\n2 - Realizar Jogada"))
        if(op == "1"):
            self.compraPecaMonte(monte)
        else:
            pass
            #  Aqui que o jogador faz suas jogadas
        
    # Need to implement
    def calculaPontuacao(self):
        return True


class Jogadores:

    def __init__(self):
        self.jogadores = list()

    def retornaJogadores(self):
        return self.jogadores

    def retornaPosicao(self, jogador):
        return self.jogadores.index(jogador)

    def retornaJogador(self, posicao):
        return self.jogadores[posicao]

    def adcionaJogador(self, jogador):
        self.jogadores.append(jogador)

    def removeJogador(self, jogador):
        return self.jogadores.pop(self.retornaPosicao(jogador))

    def adcionaJogadorPosicao(self, posicao, jogador):
        return self.jogadores.insert(posicao, jogador)

    def moveJogadorProFinal(self, jogador):
        self.adcionaJogadorPosicao(len(self.retornaJogadores()) - 1, self.removeJogador(jogador))