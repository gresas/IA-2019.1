import GameModels as gm
import PlayerModel as pm

class Round:
    def __init__(self):
        self.table = gm.Table()
        self.table_states = None

    def play(self):
        pass

class GamePlay:
    MAX_UNDO = 3

    def buildGame(self, players, score):
        self.actual_round = Round()
        self.roof_score = score
        self.round_list = list()
        self.actual_round.table.buildTable(players)
        return self

    def playTurn(self):
        self.actual_round.play()

