from . import GameModels as gm
from . import PlayerModel as pm
from .utils import util as u
import copy

class Round:
    round_score = None
    winner_player = None
    lock_player = None
    lock_game = 0

    def __init__(self):
        self.table = gm.Table()
        self.table_states = list()
        self.round_number = 1

    def play(self):
        for player in self.table.player_list.getPlayers():
            if(not self.table.turn(player, self.round_number)):
                self.lock_game += 1
                if(self.lock_game == self.table.player_list.lenPlayers()):
                    p = self.getWinnerPlayer()
                    if(p == -1):
                        self.lock_player.getHand().getGroupPieces().clear()
                    else:
                        p.getPlayerHand().getHand().getGroupPieces().clear()
                else:
                    continue
                self.lock_player = player
            if(player == self.lock_player):
                self.lock_game -= 1
                self.lock_player = None
            if(not player.getPlayerHand().getHand().getGroupPieces()):
                player.setScore(self.buildRoundScore(player))
                return player
        return ""

    def buildRoundScore(self, winner_p):
        aux_score = list()
        for player in self.table.player_list.getPlayers():
            if(player != winner_p):
                aux_score.append(player.getPlayerHand().getHand().getSumValue())
        self.round_score = max(aux_score)
        self.table_states.append(self.table)
        self.winner_player == winner_p
        return self.round_score

    def getWinnerPlayer(self):
        score_players = [(player.getPlayerHand().sumValue(), player) for player in self.table.player_list.getPlayers()]
        if(u.isTieGame(score_players)):
            return -1
        return min(score_players, key=lambda x: x[0])[1]

    def resetRound(self):
        self.table.clearTable()
        self.table.player_list.turnToNextPlayer()
        self.round_number += 1


class GamePlay:
    MAX_UNDO = 3
    roof_score = -1

    def buildGame(self, players, score):
        self.actual_round = Round()
        self.roof_score = int(score)
        self.round_list = list()
        self.players = players
        self.actual_round.table.buildTable(players)
        return self

    def playRoundTurn(self):
        winner = self.actual_round.play()
        if(winner):
            print("\nRound winner was %s\nScore: %s\n"%(winner.nick, winner.score))
            self.round_list.append(copy.deepcopy(self.actual_round))
            self.actual_round.resetRound()

    def isEnded(self):
        for player in self.actual_round.table.player_list.getPlayers():
            if(player.score >= self.roof_score):
                return player.nick
        return ""


