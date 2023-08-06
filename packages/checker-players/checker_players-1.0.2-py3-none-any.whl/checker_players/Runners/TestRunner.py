class TestRunner:

    def __init__(self, board, player1, player2, logger):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.logger = logger

    def play_single_game(self, turn_cutoff = 100):
        self.logger.begin()
        for _ in range(turn_cutoff):
            if self.board.game_over:
                break
            curr_player = self.player1 if self.board.player_turn else self.player2
            self.board.make_move(curr_player.play(self.board))
            self.logger.apply(self.board, self.player1, self.player2)
        self.logger.end(self.board, self.player1, self.player2)
        return self.logger.exit(self.board, self.player1, self.player2)

    def play_games(self, num_of_games, turn_cutoff = 100):
        for num_game in range(num_of_games):
            self.board.reset()
            self.logger.begin()
            for _ in range(turn_cutoff):
                if self.board.game_over:
                    break
                curr_player = self.player1 if self.board.player_turn else self.player2
                self.board.make_move(curr_player.play(self.board))
                self.logger.apply(self.board, self.player1, self.player2)
            self.logger.end(self.board, self.player1, self.player2)
        return self.logger.exit(self.board, self.player1, self.player2)
