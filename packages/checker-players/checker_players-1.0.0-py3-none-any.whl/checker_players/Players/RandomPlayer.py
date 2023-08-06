from checker_players.Players.Player import Player
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter
import random 
class RandomPlayer(Player):

    def play(self, board):
        return random.choice(board.get_possible_next_moves())

    # The random player does no learning
    def learn(reward, board):
        pass