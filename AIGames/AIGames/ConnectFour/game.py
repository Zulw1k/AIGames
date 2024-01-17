from math import fabs
import agents
import config
import numpy as np


class Game():
    def __init__(self):
        print('Game started!')
        
    def play_step(self, obs, buttonid=None):
        print(f"Turn: {obs.turn}")
        current_player = obs.player1 if obs.mark == 1 else obs.player2
        old_board = obs.board.copy()
        
        if buttonid is None:
            move = current_player.select_move(obs, config)
            new_grid = agents.drop_piece(obs.grid, move, obs.mark, config)
            obs.last_button_id = self.get_changed_element_id(obs.grid, new_grid)
            obs.grid = new_grid
        else:
            obs.board[buttonid] = obs.mark
            obs.grid = np.asarray(obs.board).reshape(config.rows, config.columns)
            
        obs.board = obs.grid.flatten()
        obs.is_winner, obs.winning_ids = self.check_win(obs, config, obs.mark)

        if obs.is_winner:
            obs.number_of_games += 1
            if obs.mark == 1:
                obs.player_1_wins += 1
            else:
                obs.player_2_wins += 1

        if type(current_player).__name__ == "ReinforcementAgent":
            current_player.score_move(obs, move, obs.mark, old_board, config)

        obs.turn += 1

        if obs.turn == len(obs.board) + 1:
            obs.number_of_games += 1
            obs.draws += 1
            return obs
        else:
            obs.mark = 1 if obs.mark == 2 else 2
            return obs
        
    def get_changed_element_id(self, original_grid, updated_grid):
        original_flat = original_grid.flatten()
        updated_flat = updated_grid.flatten()   
        changed_positions = np.where(original_flat != updated_flat)[0]
        if len(changed_positions) == 1:
            return changed_positions[0]   # Adding 1 to convert from 0-based to 1-based index
        else:
            return None
        

    def player_move(self, obs, buttonid):
        obs.board[buttonid] = obs.mark
        obs.grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        obs.mark = 1 if obs.mark == 2 else 2
        obs.turn = obs.turn + 1
        

    def reset(self, obs, button):    
        obs.mark = 1
        obs.board = [0 for x in range(config.columns*config.rows)]
        obs.grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        obs.turn = 1
        obs.winning_ids = []
        obs.is_winner = False
        if button:
            obs.number_of_games = 0
            obs.player_1_wins = 0
            obs.player_2_wins = 0
            obs.draws = 0
        return obs
        
    def check_win(self, obs, config, piece):
        # Initialize an empty list to store IDs of winning items
        winning_ids = []

        # horizontal
        for row in range(config.rows):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(obs.grid[row, col:col + config.inarow])
                if window.count(piece) == config.inarow:
                    # If this is a winning sequence, add IDs to the list
                    winning_ids.extend(range(row * config.columns + col, row * config.columns + col + config.inarow))
                    return True, winning_ids

        # vertical
        for row in range(config.rows - (config.inarow - 1)):
            for col in range(config.columns):
                window = list(obs.grid[row:row + config.inarow, col])
                if window.count(piece) == config.inarow:
                    # If this is a winning sequence, add IDs to the list
                    winning_ids.extend(range(row * config.columns + col, (row + config.inarow) * config.columns + col, config.columns))
                    return True, winning_ids

        # positive diagonal
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns-(config.inarow-1)):
                window = list(obs.grid[range(row, row+config.inarow), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    # If this is a winning sequence, add IDs to the list
                    winning_ids.extend(
                        range(row * config.columns + col, (row + config.inarow) * config.columns + col, config.columns + 1))
                    return True, winning_ids
                
        # negative diagonal
        for row in range(config.inarow-1, config.rows): # 4-1, 6 = 4
            for col in range(config.columns-(config.inarow-1)): # 7 - (4-1) = 4
                window = list(obs.grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    # If this is a winning sequence, add IDs to the list 
                    winning_ids.extend(range(row * config.columns + col, (row - (config.inarow-1)) * config.columns + col, -(config.columns - 1)))
                    return True, winning_ids

        return False, []
        
    def show_valid_buttons(obs, config):
        valid_moves_with_last_row = []

        for col in range(config.columns):
            row_id = None
            for row in range(config.rows - 1, -1, -1):  # Start from the bottom row and go up
                if obs.board[row * config.columns + col] == 0:
                    row_id = row * config.columns + col
                    break  # Stop searching when the first 0 is found in the column
            if row_id is not None:
                valid_moves_with_last_row.append(row_id)
        return  valid_moves_with_last_row
   
        
    
    
