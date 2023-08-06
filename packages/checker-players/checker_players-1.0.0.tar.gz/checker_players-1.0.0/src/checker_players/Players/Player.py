from checker_players.Checker_Environment.Board import Board
class Player:

    EMPTY_SPOT = Board.EMPTY_SPOT
    P1 = Board.P1
    P2 = Board.P2
    P1_K = Board.P1_K
    P2_K = Board.P2_K
    BACKWARDS_PLAYER = Board.BACKWARDS_PLAYER
    HEIGHT = Board.HEIGHT
    WIDTH = Board.WIDTH

    def __init__(self, player_number):
        self.player_number = player_number
        
    def play(self, board):
        pass

    def learn(self, reward, board):
        pass