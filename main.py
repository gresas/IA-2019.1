import pygame
from pygame.locals import *
from models.GameModels import *
from models.PieceModels import *
from models.PlayerModel import *
import sys

def init_game():
    # --------------------------------------------------------------------------------
    # Escolhendo numero de players 
    numPlayers = int(input('Quantos jogadores?\n'))

    if(numPlayers not in list(range(1, 5))):
        pygame.quit()
        print('Numero de jogadores incorreto')
        sys.exit(1)

    # Setando os nomes dos players
    jogadores = Jogadores()
    for i in range(numPlayers):
        nome = str(input('Nome do jogador %s: '%(i+1)))
        jogadores.adcionaJogador(Jogador(nome))

    numPecas = 13
    # Preenchendo monte com 106 peças
    monte = Monte()
    pecas = Pecas()
    for j in range(2):
        for i in range(numPecas):
            p = PecaAmarela((i+1))
            pecas.adcionaPeca(p)
    for j in range(2):
        for i in range(numPecas):
            p = PecaVerde((i+1))
            pecas.adcionaPeca(p)
    for j in range(2):
        for i in range(numPecas):
            p = PecaAzul((i+1))
            pecas.adcionaPeca(p)
    for j in range(2):
        for i in range(numPecas):
            p = PecaPreta((i+1))
            pecas.adcionaPeca(p)
    
    # Setando os coringas
    coringa1 = PecaCuringa(0)
    coringa2 = PecaCuringa(0)
    pecas.adcionaPeca(coringa1)
    pecas.adcionaPeca(coringa2)

    monte.atribuiPecasMonte(pecas)

    # Teste para listar dados no monte
    print('Numero de peças no monte: %s'%monte.contaPecasMonte())
    monte.embaralhaMonte()
    print(list(map(lambda x: (x.cor, x.valor), monte.retornaMonte())))
    print()

    # Distribuindo pecas para jogadores(falta a rodada de decisão da
    #  ordem de jogada)
    numPecas = 14
    print()
    for jogador in jogadores.retornaJogadores():

        for i in range(numPecas):
            jogador.compraPecaMonte(monte)
        print('Jogador: %s'%jogador.apelido)
        jogador.ordenaSuporte(2)
        print(list(map(lambda x: (x.cor, x.valor), jogador.mostraSuporte())))
        print()

    # Teste para listar dados no monte
    print()
    print('Numero de peças no monte após distribuir as peças: %s'%monte.contaPecasMonte())
    monte.embaralhaMonte()
    print(list(map(lambda x: (x.cor, x.valor), monte.retornaMonte())))

    mesa = Mesa(jogadores, monte)
    return mesa

    # --------------------------------------------------------------------------------

class Game():
    """docstring for ClassName"""
    def __init__(self):
        self.width = 300
        self.height = 280
        self.running = False
        self.mesa = init_game()

    def run(self):
        pygame.init()
        self.running = True
     
        screen = pygame.display.set_mode((self.width, self.height ) )

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))

        # Display some text
        font = pygame.font.Font(None, 36)
        text = font.render("Rummikub", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        
        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        while (self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Detecta mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.button)
            #self.mesa.turno()
            screen.blit(background, (0, 0))
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()