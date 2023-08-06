from checker_players.Players.MinimaxPlayer import MinimaxPlayer
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter
from checker_players.Checker_Environment.Board import Board

class AlphaBeta(MinimaxPlayer):    
    def get_best_board_evaluation(self, board, depth_cutoff, alpha, beta, max_step = True):
        if depth_cutoff == 0:
            return self.evaluate_board(board)

        possible_moves = board.get_possible_next_moves()

        if len(possible_moves) == 0:
            return self.evaluate_board(board)

        best_value = None
        for move in possible_moves:
            new_board = Board(board.spots, P1_turn= board.player_turn)
            new_board.make_move(move)
            value = self.get_best_board_evaluation(new_board, depth_cutoff-1, alpha, beta, max_step = max_step if (new_board.player_turn == board.player_turn) else not max_step)
            best_value = value if not best_value else best_value
            if max_step:
                best_value = max(best_value, value)
                alpha = max(alpha, value)
            else:
                best_value = min(best_value, value)
                beta = min(beta, value)

            if alpha >= beta:
                break
        
        return best_value

    def get_best_move(self, board, depth_cutoff):
        '''
        1. get all the possible moves
        2. for each move, pretend we did that move.
        3. use get_board_evaluation to see how good the move was
        4. choose the best move
        '''
        best_move = None 
        best_evaluation = float('-inf')
        alpha = float("-inf")
        beta = float("inf")

        possible_moves = board.get_possible_next_moves()

        for move in possible_moves:
            if not best_move:
                best_move = move
            new_board = Board(board.spots, P1_turn= board.player_turn)
            new_board.make_move(move)
            curr_evaluation = self.get_best_board_evaluation(new_board, depth_cutoff-1, alpha, beta, max_step = (new_board.player_turn == board.player_turn))
            best_move = move if curr_evaluation > best_evaluation else best_move
            best_evaluation = curr_evaluation if curr_evaluation > best_evaluation else best_evaluation

        return best_move

    def play(self, board):
        return self.get_best_move(board, self.depth_cutoff)

    # The Minimax player does no learning
    def learn(self, reward, board):
        pass