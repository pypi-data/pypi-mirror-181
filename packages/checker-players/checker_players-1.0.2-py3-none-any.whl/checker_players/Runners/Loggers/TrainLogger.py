from checker_players.Runners.Loggers.Logger import Logger
from checker_players.Runners.TestRunner import TestRunner 
from checker_players.Players.RandomPlayer import RandomPlayer
from checker_players.Checker_Environment.Board import Board
from checker_players.Runners.Loggers.SimpleLogger import SimpleLogger 

def evaluate_against_random_player(player1, player2):
    win_rateP1 = 0
    num_games = 100
    for i in range(num_games):
        board = Board()
        logger = Logger()
        random = RandomPlayer(board.P2)
        runner = TestRunner(board, player1, random, logger)
        runner.play_single_game(1000)
        winner = board.Current_Winner
        win_rateP1 = win_rateP1 + 1/num_games if winner == board.P1 else win_rateP1

    win_rateP2 = 0
    for i in range(num_games):
        board = Board()
        logger = Logger()
        random = RandomPlayer(board.P1)
        runner = TestRunner(board, random, player2, logger)
        runner.play_single_game(1000)
        winner = board.Current_Winner
        win_rateP2 = win_rateP2 + 1/num_games if winner == board.P2 else win_rateP2
    
    return win_rateP1, win_rateP2



class TrainLogger(Logger):
    winner_history = []
    current_game_number = 0
    player1WRHistory = []
    player2WRHistory = []


    def __init__(self):
        pass

    def begin(self):
        pass

    def apply(self, board, player1, player2):
        if board.is_game_over():
            self.winner_history.append(board.P1 if (board.player_turn) and board.get_possible_next_moves() else board.P2)

    def end(self, board, player1, player2):
        self.current_game_number += 1
        if self.current_game_number % 100 == 0:
            player1WR, player2WR = evaluate_against_random_player(player1, player2)
            self.player1WRHistory.append(player1WR)
            self.player2WRHistory.append(player2WR)


    def exit(self, board, player1, player2):
        return self.current_game_number, self.winner_history, self.player1WRHistory, self.player2WRHistory