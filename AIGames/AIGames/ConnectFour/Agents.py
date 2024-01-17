import random
from collections import deque
import numpy as np
import pickle

# Selects random valid column
class Player:
    def __init__(self):
        pass
        

class AgentRandom:
    def __init__(self):
        pass

    def select_move(self, obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        return random.choice(valid_moves)

class AgentMiddle:
    def __init__(self):
        pass

    def select_move(self, obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        middle_index = len(valid_moves) // 2
        return valid_moves[middle_index] if len(valid_moves) % 2 != 0 else valid_moves[middle_index - 1]

class AgentLeftmost:
    def __init__(self):
        pass

    def select_move(self, obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        return valid_moves[0]

class AgentV1:
    def __init__(self):
        pass

    def select_move(self, obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        for valid_move in valid_moves:
            if check_winning_move(obs, config, valid_move, piece=obs.mark):
                return valid_move
        return random.choice(valid_moves)

class AgentV2:
    def __init__(self):
        pass

    def select_move(self, obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        for col in valid_moves:
            if check_winning_move(obs, config, col, piece=obs.mark) or check_winning_move(obs, config, col, piece=obs.mark % 2 + 1):
                return col
        return random.choice(valid_moves)

class HeuresticAgent:
    def __init__(self):
        pass
    
    def select_move(self, obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        # Use the heuristic to assign a score to each possible board in the next turn
        scores = dict(zip(valid_moves, [score_move(grid, col, obs.mark, config) for col in valid_moves]))
        print(scores)
        # Get a list of columns (moves) that maximize the heuristic
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        return random.choice(max_cols)
    
class MinmaxAgent:
    def __init__(self):
        pass
    
    def select_move(self, obs, config, N_STEPS=3):
        # Get list of valid moves
        valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
        # Convert the board to a 2D grid
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        # Use the heuristic to assign a score to each possible board in the next step
        scores = dict(zip(valid_moves, [score_move(grid, col, obs.mark, config, N_STEPS) for col in valid_moves]))
        # Get a list of columns (moves) that maximize the heuristic
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        # Select at random from the maximizing columns
        return random.choice(max_cols)
    

class ReinforcementAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.05):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.q_table = self.load_q_table('q_table.pkl')
        
    def save_q_table(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.q_table, file)

    def load_q_table(self, filename):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            # If the file is not found or empty, return an empty dictionary
            return {}

    def select_move(self, obs, config):
        if np.random.rand() < self.exploration_prob:
            print("Go Random")
            print(np.random.rand()," vs ",self.exploration_prob)
            # Exploration: Choose a random move
            return random.choice([col for col in range(config.columns) if obs.board[col] == 0])
        else:
            print("Go q")
            print(np.random.rand()," vs ",self.exploration_prob)
            # Exploitation: Choose among the maximum Q-values
            state_key = tuple(obs.board)  # Convert the board state to a hashable tuple
            print(f"state key: {state_key}")
            q_values = self.q_table.get(state_key, {})
            if not q_values:
                print("random move")
                print(f"q values {q_values}")
                return random.choice([col for col in range(config.columns) if obs.board[col] == 0])
            else:
                print(f"q values {q_values}")
                max_key = max(q_values, key=q_values.get)
                first_element_of_max_key = max_key[0]
                print(f"max_key {max_key}")
                return first_element_of_max_key #return col id where value is highest

    def update_q_value(self, state, action, reward, next_state):
        print(f"Updatating reward: {reward}")
        state_key = tuple(state)
        action_key = tuple(action)
        next_state_key = tuple(next_state)
        print(action_key)

        # Initialize Q-values for the state if not present
        self.q_table.setdefault(state_key, {})

        # Update the Q-value using the Q-learning update rule
        current_q_value = self.q_table[state_key].get(action_key, 0)
        max_future_q_value = max(self.q_table.get(next_state_key, {}).values(), default=0)
        new_q_value = (1 - self.learning_rate) * current_q_value + \
                      self.learning_rate * (reward + self.discount_factor * max_future_q_value)

        # Update the Q-value in the Q-table
        self.q_table[state_key][action_key] = new_q_value
        self.save_q_table('q_table.pkl')
        
    def score_move(self, obs, col, mark, old_board, config):
        action = (col, mark)
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        if type(obs.player1).__name__ == "ReinforcementAgent" and obs.mark ==1:
            if obs.is_winner:
                obs.player1.update_q_value(old_board, action, 100, obs.grid.flatten())
                print("Scored 100")
            elif any(check_winning_move(obs, config, col, obs.mark % 2 + 1) for col in valid_moves):  # Check if player 2 can win
                obs.player1.update_q_value(old_board, action, -50, obs.grid.flatten())
                print("Scored -50")
            elif np.array_equal(np.count_nonzero(old_board == 0), np.count_nonzero(obs.board == 0)):
                obs.player1.update_q_value(old_board, action, -100000, obs.grid.flatten())
                print("Scored -100000")
            else:
                obs.player1.update_q_value(old_board, action, 1, obs.grid.flatten())
                print("Scored 1")

        if type(obs.player2).__name__ == "ReinforcementAgent" and obs.mark ==2:
            if obs.is_winner and obs.mark == 2:
                obs.player2.update_q_value(old_board, action, 100, obs.grid.flatten())
            elif any(check_winning_move(obs, config, col, obs.mark % 2 + 1) for col in valid_moves):  # Check if player 1 can win
                obs.player2.update_q_value(old_board, action, -50, obs.grid.flatten())
            elif np.array_equal(np.count_nonzero(old_board == 0), np.count_nonzero(obs.board == 0)):
                obs.player2.update_q_value(old_board, action, -100000, obs.grid.flatten())
                print("Scored -100000")
            else:
                obs.player2.update_q_value(old_board, action, 1, obs.grid.flatten())    
    
class AlphabetaAgent:
    def __init__(self):
        pass
    
    def select_move(self, obs, config, N_STEPS=4):
        # Get list of valid moves
        valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
        # Convert the board to a 2D grid
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        # Use the heuristic to assign a score to each possible board in the next step
        scores = dict(zip(valid_moves, [score_move(grid, col, obs.mark, config, N_STEPS,algorithm='alphabeta') for col in valid_moves]))
        # Get a list of columns (moves) that maximize the heuristic
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        # Select at random from the maximizing columns
        return random.choice(max_cols)
   
    
        



#agent dict
agent_dict = {"Human": Player(),
              "Agent random": AgentRandom(),
              "Agent middle": AgentMiddle(),
              "Agent leftmost": AgentLeftmost(),
              "Agent V1": AgentV1(),
              "Agent V2": AgentV2(),
              "Agent Heurestic": HeuresticAgent(),
              "Agent MinMax": MinmaxAgent(),
              "Agent Alphabeta": AlphabetaAgent(),
              "ReinforcementAI": ReinforcementAgent()
              }



# Agents functions
# Alphabeta implementation
def alphabeta(node, depth, maximizingPlayer, mark, config, alpha=-np.Inf, beta=np.Inf):
    is_terminal = is_terminal_node(node, config)
    valid_moves = [c for c in range(config.columns) if node[0][c] == 0]
    if depth == 0 or is_terminal:
        return get_heuristic(node, mark, config)
    if maximizingPlayer:
        value = -np.Inf
        for col in valid_moves:
            child = drop_piece(node, col, mark, config)
            value = max(value, minimax(child, depth-1, False, mark, config))
            alpha = max(alpha, value)
        return value
    else:
        value = np.Inf
        for col in valid_moves:
            child = drop_piece(node, col, mark%2+1, config)
            value = min(value, minimax(child, depth-1, True, mark, config))
            if value < alpha:
                break
            beta = min(beta, value)
        return value
    
# Helper function for minimax: checks if agent or opponent has four in a row in the window
def is_terminal_window(window, config):
    return window.count(1) == config.inarow or window.count(2) == config.inarow

# Helper function for minimax: checks if game has ended
def is_terminal_node(grid, config):
    # Check for draw 
    if list(grid[0, :]).count(0) == 0:
        return True
    # Check for win: horizontal, vertical, or diagonal
    # horizontal 
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if is_terminal_window(window, config):
                return True
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if is_terminal_window(window, config):
                return True
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if is_terminal_window(window, config):
                return True
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if is_terminal_window(window, config):
                return True
    return False

# Minimax implementation
def minimax(node, depth, maximizingPlayer, mark, config):
    is_terminal = is_terminal_node(node, config)
    valid_moves = [c for c in range(config.columns) if node[0][c] == 0]
    if depth == 0 or is_terminal:
        return get_heuristic(node, mark, config)
    if maximizingPlayer:
        value = -np.Inf
        for col in valid_moves:
            child = drop_piece(node, col, mark, config)
            value = max(value, minimax(child, depth-1, False, mark, config))
        return value
    else:
        value = np.Inf
        for col in valid_moves:
            child = drop_piece(node, col, mark%2+1, config)
            value = min(value, minimax(child, depth-1, True, mark, config))
        return value
    
# Helper function for get_heuristic: checks if window satisfies heuristic conditions
def check_window(window, num_discs, piece, config):
    return (window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs)

# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
def count_windows(grid, num_discs, piece, config):
    num_windows = 0
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    return num_windows

# Helper function for score_move: calculates value of heuristic for grid
def get_heuristic(grid, mark, config):
    num_threes = count_windows(grid, 3, mark, config)
    num_fours = count_windows(grid, 4, mark, config)
    num_threes_opp = count_windows(grid, 3, mark%2+1, config)
    num_fours_opp = count_windows(grid, 4, mark%2+1, config)
    score = num_threes - 1e2*num_threes_opp - 1e4*num_fours_opp + 1e6*num_fours
    return score

# Calculates score if agent drops piece in selected column
def score_move(grid, col, mark, config, nsteps=None, algorithm=None):
    next_grid = drop_piece(grid, col, mark, config)
    if nsteps:
        if algorithm:
            score = alphabeta(next_grid, nsteps-1, False, mark, config)
        else:
            score = minimax(next_grid, nsteps-1, False, mark, config)
    else:
        score = get_heuristic(next_grid, mark, config)
    return score

# Gets board at next step if agent drops piece in selected column
def drop_piece(grid, col, piece, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = piece
    return next_grid

# Returns True if dropping piece in column results in game win
def check_winning_move(obs, config, col, piece):
    # Convert the board to a 2D grid
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    next_grid = drop_piece(grid, col, piece, config)
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[row,col:col+config.inarow])
            if window.count(piece) == config.inarow:
                return True
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(next_grid[row:row+config.inarow,col])
            if window.count(piece) == config.inarow:
                return True
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    return False