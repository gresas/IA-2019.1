from . import GameModels as gm
from . import PlayerModel as pm

class Round:
    round_score = None
    
    def __init__(self):
        self.table = gm.Table()
        self.table_states = list()

    def play(self):
        for player in self.table.player_list.getPlayers():
            self.table.turn(player)

class GamePlay:
    MAX_UNDO = 3
    roof_score = -1

    def buildGame(self, players, score):
        self.actual_round = Round()
        self.roof_score = score
        self.round_list = list()
        self.actual_round.table.buildTable(players)
        return self

    def playRoundTurn(self):
        self.actual_round.play()

