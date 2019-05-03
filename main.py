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
    players = Players()
    for i in range(numPlayers):
        name = str(input('Nome do jogador %s: '%(i+1)))
        players.appendPlayer(Player(name))

    num_pieces = 7
    # Preenchendo monte com 28 peças
    heap = Heap()
    pieces = GroupPieces()
    
    #for k in range(4):
    for i in range(num_pieces):
        for j in range(i, num_pieces):
            p = Piece(i, j)
            pieces.appendPiece(p)

    heap.setHeap(pieces)

    # Teste para listar dados no monte
    print('Numero de peças no monte: %s'%heap.len())
    heap.shuffleHeap()
    print(list(map(lambda x: (x.left_value, x.right_value), heap.getHeap().getGroupPieces())))
    print()

    # Distribuindo pecas para jogadores(falta a rodada de decisão da
    #  ordem de jogada)
    num_pieces = 7
    print()
    for p in players.getPlayers():
        for i in range(num_pieces):
            p.buy(heap)
        print('Jogador: %s'%p.getName())
        #p.sortHand()
        print(list(map(lambda x: (x.left_value, x.right_value), p.getPlayerHand().getHand().getGroupPieces())))
        print()

    # Teste para listar dados no monte
    print()
    print('Numero de peças no monte após distribuir as peças: %s'%heap.len())
    heap.shuffleHeap()
    print(list(map(lambda x: (x.left_value, x.right_value), heap.getHeap().getGroupPieces())))

    table = Table(players, heap)
    return table 

    # --------------------------------------------------------------------------------

class Game():
    """docstring for ClassName"""
    def __init__(self):
        self.width = 300
        self.height = 280
        self.running = False
        self.table = init_game()

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
        text = font.render("Domino", 1, (10, 10, 10))
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
            ''' 
                # Detecta mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.button)
            #self.mesa.turno()
            screen.blit(background, (0, 0))
            pygame.display.flip()
            '''

if __name__ == "__main__":
    game = Game()
    game.run()