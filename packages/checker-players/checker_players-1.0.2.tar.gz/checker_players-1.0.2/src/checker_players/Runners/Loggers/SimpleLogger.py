from checker_players.Runners.Loggers.Logger import Logger
import time
import copy

'''
This simple Logger notes who won the game, how many turns the game took to terminate, 
the board state at each turn, and how much time each each turn took. If the "winner of the game"
is set to None then that implies that the game did not terminate. 
'''

class SimpleLogger(Logger):
    winner = None
    current_turn_number = 0
    board_state_history = []
    board_time_per_move_history = []

    time_at_last_move = None

    def __init__(self):
        pass

    def begin(self):
        self.time_at_last_move = time.process_time()

    def apply(self, board, player1, player2):
        self.current_turn_number += 1

        self.board_state_history.append(copy.deepcopy(board.spots))

        self.board_time_per_move_history.append(time.process_time() - self.time_at_last_move)
        self.time_at_last_move = time.process_time()

    def end(self, board, player1, player2):
        self.winner = board.Current_Winner
        pass

    def exit(self, board, player1, player2):
        return self.winner, self.current_turn_number, self.board_state_history, self.board_time_per_move_history