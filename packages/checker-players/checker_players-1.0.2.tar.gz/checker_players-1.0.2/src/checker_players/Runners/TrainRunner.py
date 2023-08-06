import numpy as np

class TrainRunner:

    def __init__(self, board, player1, player2, logger):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.logger = logger

    def learn_games_for_player1(self, num_of_games, turn_cutoff = 100):
        for num_game in range(num_of_games):
            self.board.reset_board()
            self.logger.begin()
            board_states = []
            winner = None
            for _ in range(turn_cutoff):
                if self.board.is_game_over:
                    winner = self.board.Current_Winner
                    break
                if self.board.player_turn:
                    board_states.append(self.board.spots)
                curr_player = self.player1 if self.board.player_turn else self.player2
                self.board.make_move(curr_player.play(self.board))
                self.logger.apply(self.board, self.player1, self.player2)
            self.logger.end()
            self.player1.learn(winner, board_states)
        return self.logger.exit()

    def learn_games(self, num_of_games, turn_cutoff = 100):
        for num_game in range(num_of_games):
            if num_game % 100 == 0:
                print(num_game)
            self.board.reset_board()
            self.logger.begin()
            board_states_p1 = []
            board_states_p2 = []
            winner = None
            for _ in range(turn_cutoff):
                if self.board.game_over:
                    winner = self.board.Current_Winner
                    break
                if self.board.player_turn:
                    board_states_p1.append(self.board.spots)
                else:
                    board_states_p2.append(self.board.spots)
                curr_player = self.player1 if self.board.player_turn else self.player2
                self.board.make_move(curr_player.play(self.board))
                self.logger.apply(self.board, self.player1, self.player2)
            self.logger.end(self.board, self.player1, self.player2)
            self.player1.learn(winner, board_states_p1)
            self.player2.learn(winner, board_states_p2)
        return self.logger.exit(self.board, self.player1, self.player2)