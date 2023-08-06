from checker_players.Players.Player import Player
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter
from checker_players.Checker_Environment.Board import Board
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter

class MinimaxPlayer(Player):
    def __init__(self, player_number, depth_cutoff = 3):
        super().__init__(player_number)
        self.depth_cutoff = depth_cutoff

    def evaluate_board(self, board):
        doubleColumn = DoubleColumnInterpretter().interpret(board)
        friendly_pieces = doubleColumn[self.player_number]
        enemy_pieces = doubleColumn[board.P2 if self.player_number == board.P1 else board.P1]

        return len(friendly_pieces) - len(enemy_pieces)
    
    def get_best_board_evaluation(self, board, depth_cutoff, max_step = True):
        if depth_cutoff == 0:
            return self.evaluate_board(board)

        possible_moves = board.get_possible_next_moves()

        if len(possible_moves) == 0:
            return self.evaluate_board(board)

        best_child_board_evaluations = []
        for move in possible_moves:
            new_board = Board(board.spots, P1_turn= board.player_turn)
            new_board.make_move(move)
            best_child_board_evaluations.append(self.get_best_board_evaluation(new_board, depth_cutoff-1, max_step = max_step if (new_board.player_turn == board.player_turn) else not max_step))
        
        return max(best_child_board_evaluations) if max_step else min(best_child_board_evaluations)

    def get_best_move(self, board, depth_cutoff):
        '''
        1. get all the possible moves
        2. for each move, pretend we did that move.
        3. use get_board_evaluation to see how good the move was
        4. choose the best move
        '''
        best_move = None 
        best_evaluation = float('-inf')

        possible_moves = board.get_possible_next_moves()

        for move in possible_moves:
            if not best_move:
                best_move = move
            new_board = Board(board.spots, P1_turn= board.player_turn)
            new_board.make_move(move)
            curr_evaluation = self.get_best_board_evaluation(new_board, depth_cutoff-1, max_step = (new_board.player_turn == board.player_turn))
            best_move = move if curr_evaluation > best_evaluation else best_move
            best_evaluation = curr_evaluation if curr_evaluation > best_evaluation else best_evaluation

        return best_move

    def play(self, board):
        return self.get_best_move(board, self.depth_cutoff)

    # The Minimax player does no learning
    def learn(self, reward, board):
        pass