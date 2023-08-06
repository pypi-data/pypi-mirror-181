from checker_players.Players.Player import Player
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter
from checker_players.Checker_Environment.Board import Board
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter

#from tensorflow import keras
#from tensorflow.keras import layers as kl

import torch
import torch.nn as nn

import numpy as np

class DQNPlayer(Player):
    def __init__(self, player_number, model=0): #I think we want a shallow copy of model
        super().__init__(player_number)
        
        self.model = model
        if not self.model:
            self.model = self.create_model()
        
        
    def get_best_move(self, board):
        possible_moves = board.get_possible_next_moves()
        q_values = np.array((possible_moves))
        for i, move in enumerate(possible_moves):
            q_values[i] = self.model(move)
        return possible_moves(np.argmax(q_values))
        
        
    def play(self, board):
        return self.get_best_move(board)
    
    
    def learn(self, logger_exit, reward, learning_rate = 0.01):
        winner, current_turn_number, board_state_history, _ = logger_exit
        for turn, board in enumerate(board_state_history):
            y_pred = self.model(board)
            loss = reward[turn-1]
            self.model.zero_grad()
            loss.backward()
            
            with torch.no_grad():
                for param in self.model.parameters():
                    param -= learning_rate * param.grad
        
    
    def create_model(self):
        model = torch.nn.Sequential(
            [
                #we can make the input 32, since half of all pieces are empty
                nn.Flatten(input_shape=(8, 8)),
                nn.Linear(64, 32), nn.ReLU(),
                nn.Linear(32, 16), nn.ReLU(),
                nn.Linear(16,  8), nn.ReLU(),
                nn.Linear( 8,  4), nn.ReLU(),
                nn.Linear( 4,  1)
            ]
        )
        return model
        
        
        