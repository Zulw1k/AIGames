import config
import numpy as np
import agents

mark = 1
board = [0 for x in range(config.columns*config.rows)]
grid = np.asarray(board).reshape(config.rows, config.columns)
number_of_games = 0
player_1_wins = 0
player_2_wins = 0
draws = 0
turn = 1
reward = 0

player1 = agents.agent_dict["Human"]
player2 = agents.agent_dict["Human"]
last_button_id = None
winning_ids = []
is_winner = False


