from checker_players.Interpretters.Interpretter import Interpretter

class FlatFeaturesInterpretter(Interpretter):
    def interpret(self, board_state):
        features = []
        for x, row in enumerate(board_state):
            for y, element in enumerate(row):
                if (x+y) % 2 == 1:
                    features.append(board_state[x][y])
        return features