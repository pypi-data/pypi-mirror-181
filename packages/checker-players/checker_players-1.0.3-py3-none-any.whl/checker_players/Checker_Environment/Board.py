"""
-Should store moves as array of locations e.g.: [[x1,y1],[x2,y2]]
if self.player_turn == True then it is player 1's turn
"""
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter
import copy
class Board:
    """
    A class to represent and play an 8x8 game of checkers.
    """
    EMPTY_SPOT = 0
    P1 = 1
    P2 = 2
    P1_K = 3
    P2_K = 4
    BACKWARDS_PLAYER = P2
    HEIGHT = 8
    WIDTH = 8

    Current_Winner = 0
    game_over = False
    
    def __init__(self, board_state=None, P1_turn=True):
        """
        Initializes a new instance of the Board class.  Unless specified otherwise, 
        the board will be created with a start board configuration.
        """
        self.player_turn = P1_turn 
        self.spots = [ [self.EMPTY_SPOT] * self.WIDTH for _ in range(self.HEIGHT)]
        
        if board_state is None:
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):   
                    if y<3 and (x+y)%2==1:
                        self.spots[x][y] = self.P1
                    elif y>4 and (x+y)%2==1:
                        self.spots[x][y] = self.P2
        else:
            self.spots = copy.deepcopy(board_state)

    def reset_board(self):
        """
        Resets the current configuration of the game board to the original 
        starting position.
        """
        self.spots = Board().spots
        self.Current_Winner = 0
        self.game_over = False
        
    def empty_board(self):
        """
        Removes any pieces currently on the board and leaves the board with nothing but empty spots.
        """
        self.spots = [ [self.EMPTY_SPOT] * self.WIDTH for _ in range(self.HEIGHT)]
    
    def is_game_over(self):
        """
        Finds out and returns whether the game currently being played is over or
        not.
        """
        player1_pieces = [[x,y] for x in range(self.WIDTH) for y in range(self.HEIGHT) if self.get_spot_info([x,y]) in (self.P1, self.P1_K)]
        player2_pieces = [[x,y] for x in range(self.WIDTH) for y in range(self.HEIGHT) if self.get_spot_info([x,y]) in (self.P2, self.P2_K)]

        possible_moves = self.get_possible_next_moves()

        return (not player1_pieces) or (not player2_pieces) or (not possible_moves)

    def is_spot(self, loc):
        """
        Finds out of the spot at the given location is an actual spot on the game board.
        """
        return loc[0] >= 0 and loc[0] < self.WIDTH and loc[1] >= 0 and loc[1] < self.HEIGHT
      
    def get_spot_info(self, loc):
        """
        Gets the information about the spot at the given location.
        """
        return self.spots[loc[0]][loc[1]]
       
    def forward_n_locations(self, start_loc, n, backwards=False):
        """
        Gets the locations possible for moving a piece from a given location diagonally
        forward (or backwards if wanted) a given number of times(without directional change midway).  
        """
        if backwards:
            return [[start_loc[0]+(x_parity*n), start_loc[1]+(-1*n)] for x_parity in [1,-1]]
        else:
            return [[start_loc[0]+(x_parity*n), start_loc[1]+(n)] for x_parity in [1,-1]]
    
    def is_king(self, loc):
        piece = self.spots[loc[0]][loc[1]]
        return piece == self.P1_K or piece == self.P2_K

    def is_backwards_player(self, loc):
        piece = self.spots[loc[0]][loc[1]]
        return piece == self.BACKWARDS_PLAYER

    def is_empty(self, loc):
        piece = self.spots[loc[0]][loc[1]]
        return piece == self.EMPTY_SPOT
    
    def get_simple_moves(self, start_loc):
        """    
        Gets the possible moves a piece can make given that it does not capture any opponents pieces.
        
        PRE-CONDITION:
        -start_loc is a location with a players piece
        """
        
        next_locations = []
        if self.is_king(start_loc):
            next_locations = self.forward_n_locations(start_loc, 1)
            next_locations.extend(self.forward_n_locations(start_loc, 1, backwards=True))
        elif self.is_backwards_player(start_loc):
            next_locations = self.forward_n_locations(start_loc, 1, backwards=True)
        else:
            next_locations = self.forward_n_locations(start_loc, 1)
        

        possible_next_locations = [loc for loc in next_locations if self.is_spot(loc) and self.is_empty(loc)]
            
        return [[start_loc, end_spot] for end_spot in possible_next_locations]   
       
    def are_opponents(self, loc1, loc2):
        piece1 = self.spots[loc1[0]][loc1[1]]
        piece2 = self.spots[loc2[0]][loc2[1]]
        if (piece1 == self.P1 or piece1 == self.P1_K):
            return piece2 == self.P2 or piece2 == self.P2_K 
        else:
            return piece2 == self.P1 or piece2 == self.P1_K      
 
    def get_capture_moves(self, start_loc):
        """
        Get all of the possible moves for a piece which involve capturing an opponent's piece.
        """
            
        answer = []
        next1 = []
        next2 = []
        
        if self.is_king(start_loc):  
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc, 2)
            next1.extend(self.forward_n_locations(start_loc, 1, True))
            next2.extend(self.forward_n_locations(start_loc, 2, True))
        elif self.is_backwards_player(start_loc):
            next1 = self.forward_n_locations(start_loc, 1, True)
            next2 = self.forward_n_locations(start_loc, 2, True)
        else:
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc, 2)

        for loc1, loc2 in zip(next1, next2):
            if self.is_spot(loc1) and self.is_spot(loc2) and self.is_empty(loc2) and self.are_opponents(start_loc, loc1):
                capture_move = [start_loc, loc2]
                answer.append(capture_move)
                            
        return answer
        
    def get_possible_next_moves(self):
        """
        Gets the possible moves that can be made from the current board configuration.
        """
        flat_map = lambda xs: [y for ys in xs for y in ys]
        double_column = DoubleColumnInterpretter().interpret(self)
        current_pieces = double_column[self.P1 if self.player_turn else self.P2]
        
        simple_moves = flat_map([self.get_simple_moves(loc) for loc in current_pieces if self.get_simple_moves(loc) != []])
        capture_moves = flat_map([self.get_capture_moves(loc) for loc in current_pieces if self.get_capture_moves(loc) != []])
        return simple_moves + capture_moves 

    def get_kings_row_positions(self, player):
        if player == self.BACKWARDS_PLAYER:
            return [[i, 0] for i in range(self.WIDTH)]
        elif player in (self.P1, self.P2):
            return [[i, self.HEIGHT-1] for i in range(self.WIDTH)]
        else:
            raise ValueError("Not a valid player number. Availible player numbers are: " +str(self.P1)+", "+str(self.P2))

    def make_move(self, move, switch_player_turn=True):
        """
        Makes a given move on the board, and (as long as is wanted) switches the indicator for
        which players turn it is.
        """
        init_loc = move[0]
        final_loc = move[1]
        current_player = self.P1 if self.player_turn else self.P2

        # Here we are just making sure that the right player is moving their piece
        if (self.get_spot_info(init_loc) in (self.P1, self.P1_K) and not self.player_turn) or (self.get_spot_info(init_loc) in (self.P2, self.P2_K) and self.player_turn):
            raise ValueError("Piece of type " + str(self.get_spot_info(init_loc)) + " was attempted to move while Board.switch_player_turn = " + str(self.player_turn))

        if move in self.get_simple_moves(init_loc):
            self.spots[final_loc[0]][final_loc[1]] = self.get_spot_info(init_loc)
            self.spots[init_loc[0]][init_loc[1]] = self.EMPTY_SPOT

            # Here we are promoting a checker piece if it has reached it's king row
            if final_loc in self.get_kings_row_positions(self.P1 if self.player_turn else self.P2):
                self.spots[final_loc[0]][final_loc[1]] = self.P1_K if self.player_turn else self.P2_K

            if switch_player_turn:
                self.player_turn = not self.player_turn

        elif move in self.get_capture_moves(init_loc):
            distx = final_loc[0]-init_loc[0]
            disty = final_loc[1]-init_loc[1]
            enemy_piece_loc = [(distx)//2 + init_loc[0], (disty)//2 + init_loc[1]]
            
            self.spots[final_loc[0]][final_loc[1]] = self.spots[init_loc[0]][init_loc[1]]
            self.spots[init_loc[0]][init_loc[1]] = self.EMPTY_SPOT
            self.spots[enemy_piece_loc[0]][enemy_piece_loc[1]] = self.EMPTY_SPOT

            # Here we are promoting a checker piece if it has reached it's king row
            if final_loc in self.get_kings_row_positions(self.P1 if self.player_turn else self.P2):
                self.spots[final_loc[0]][final_loc[1]] = self.P1_K if self.player_turn else self.P2_K

        else:
            raise ValueError("Not a legal move.")

        if (self.is_game_over()):
            self.Current_Winner = current_player
            self.game_over = True

    def get_potential_spots_from_moves(self, moves):
        """
        Get's the potential spots for the board if it makes any of the given moves.
        If moves is None then returns it's own current spots.
        """
        if moves is None:
            return self.spots
        potential_spots = []
        for move in moves:
            newBoard = Board(self.spots)
            newBoard.make_move(move)
            potential_spots.append(newBoard.spots) 
        return potential_spots
        
    def insert_pieces(self, pieces_info):
        """
        Inserts a set of pieces onto a board.

        pieces_info is in the form: [[x1, y1, piece1], [x2, y2, piece2], ..., [xn, yn, piecen]]
        """
        for piece_info in pieces_info:          
            self.spots[piece_info[0]][piece_info[1]] = piece_info[2]
        
    def get_symbol(self, location):
        """
        Gets the symbol for what should be at a board location.
        """
        if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
            return " "
        elif self.spots[location[0]][location[1]] == self.P1:
            return "o"
        elif self.spots[location[0]][location[1]] == self.P2:
            return "x"
        elif self.spots[location[0]][location[1]] == self.P1_K:
            return "O"
        elif self.spots[location[0]][location[1]] == self.P2_K:
            return "X"
        else:
            raise ValueError("Not a valid player number. Availible player numbers are: " +str(self.P1)+", "+str(self.P2))
    
    def print_board(self):
        """
        Prints a string representation of the current game board.
        """
        norm_line = "|-----|-----|-----|-----|-----|-----|-----|-----|"
        print(norm_line)
        for j in range(self.HEIGHT):
            row = "|  "
            for i in range(self.WIDTH):
                row = row + self.get_symbol([i, j]) + "  |  "
            print(row)
            print(norm_line)            