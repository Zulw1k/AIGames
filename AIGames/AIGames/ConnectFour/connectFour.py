import pygame
import buttons
import config
import sys
import time

sys.path.append('C:/Users/Wojtek/source/repos/AIGames/AIGames/ConnectFour/')
from ConnectFour import obs, agents



class ConnectFour():
    def __init__(self, aigames_instance=None, game_instance=None):
        self.aigames_instance = aigames_instance
        self.game_instance = game_instance
        self.pause = True
        # other variables
    
    def start(self):
        # init display
        pygame.init()

        # set up display
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption('ConnectFour')
        # Define fonts
        self.mainfont = pygame.font.SysFont('arialblack', 15)
        self.subfont = pygame.font.SysFont('arialblack', 10)
        
        # create text
        self.maintitle_text = buttons.Text(x=200, y=5, text="Connect Four", font=self.mainfont, screen=self.screen)
        self.player1_text = buttons.Text(x=500, y=280, text="Player 1", font=self.mainfont, screen=self.screen)
        self.player2_text = buttons.Text(x=650, y=280, text="Player 2", font=self.mainfont, screen=self.screen)
        
        # create editable text
        self.playermove_text = buttons.Text(x=30, y=420, text=f"Player move: {obs.mark}", font=self.mainfont, screen=self.screen)
        self.result_text = buttons.Text(x=250, y=460, text=f"Result: {obs.player_1_wins} - {obs.draws} - {obs.player_2_wins}", font=self.mainfont, screen=self.screen)
        self.games_count_text = buttons.Text(x=30, y=460, text=f"Games count: {obs.number_of_games}", font=self.mainfont, screen=self.screen)
        self.playerturn_text = buttons.Text(x=250, y=420, text=f"Current turn: {obs.turn}", font=self.mainfont, screen=self.screen)     

        # create individual buttons
        self.b1=buttons.Button(target_instance=self, target_method='press_play_button', x=500, y=20, width=130, height=50, args=(obs,), screen=self.screen, text="Bot move")
        self.b2=buttons.Button(target_instance=self, target_method='automove', x=500, y=40+50, width=130, height=50, screen=self.screen, text="Automove")
        self.b3=buttons.Button(target_instance=self, target_method='return_to_main_menu', x=650, y=20, width=130, height=50, screen=self.screen, text="Return to menu")
        self.b4=buttons.Button(target_instance=self, target_method='exit_game', x=500, y=80+150, width=130, height=50, screen=self.screen, text="Exit")
        self.b5=buttons.Button(target_instance=self, target_method='reset', x=650, y=80+150, width=130, height=50, args=(obs, True), screen=self.screen, text="Reset board")

        # create a button grid
        self.button_grid = buttons.ButtonGrid(rows=config.rows, cols=config.columns, button_radius=25, screen=self.screen, margin=10)
        
        # Listbox
        self.dropbox_p1 = buttons.DropdownSelect(x=500, y=100+200, width=130, height=50, player=1, options=list(agents.agent_dict.keys()), screen=self.screen)
        self.dropbox_p2 = buttons.DropdownSelect(x=650, y=100+200, width=130, height=50, player=2, options=list(agents.agent_dict.keys()), screen=self.screen)
        
        # main game loop              
        self.running = True
        while self.running:
            # def changeable text       
            self.playermove_text.text = f"Player turn: {obs.mark}"
            self.playerturn_text.text = f"Current turn: {obs.turn}"
            self.result_text.text = f"Result: {obs.player_1_wins} - {obs.draws} - {obs.player_2_wins}"
            self.games_count_text.text = f"Games count: {obs.number_of_games}"
            


            if self.pause == False:
                pygame.display.flip()
                self.press_play_button(obs)
            
            # Event handler    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        self.b1.handle_click(pos)
                        self.b2.handle_click(pos)
                        self.b3.handle_click(pos)
                        self.b4.handle_click(pos)
                        self.b5.handle_click(pos)
                        self.dropbox_p1.handle_click(pos)
                        self.dropbox_p2.handle_click(pos)
                        clicked_button = self.button_grid.handle_click(pos, obs.mark)
                        if clicked_button is not None:
                            self.human_button_grid_press(obs, clicked_button)  
                            
            if (type(obs.player1).__name__ == "Player" and obs.mark ==1) or\
                (type(obs.player2).__name__ == "Player" and obs.mark ==2):
                valid_moves = self.show_valid_buttons(obs, config)
                self.button_grid.show_valid_buttons(valid_moves)
            else:
                self.button_grid.disable_buttons() 



            # Draw features on the screen
            self.screen.fill((60, 70, 90)) 
            self.b1.draw()
            self.b2.draw()
            self.b3.draw()
            self.b4.draw()
            self.b5.draw()
            self.maintitle_text.draw()
            self.playerturn_text.draw()
            self.games_count_text.draw()
            self.player2_text.draw()
            self.player1_text.draw()
            self.playermove_text.draw()
            self.button_grid.draw()  
            self.result_text.draw()
            self.dropbox_p1.draw()
            self.dropbox_p2.draw() 


            
            if obs.is_winner:
                self.button_grid.change_borders_to_blue(list(obs.winning_ids))
                #time.sleep(1)
                self.reset(obs)
            elif obs.turn == len(obs.board) + 1:
                self.reset(obs)
            pygame.display.flip()  

  
        pygame.quit()
        sys.exit()          
        
    def human_button_grid_press(self, obs, clicked_button):
        obs = self.game_instance.play_step(obs, clicked_button)
        return obs
        
    def press_play_button(self, obs):
        if type(obs.player1).__name__ == "Player" and obs.mark == 1 or type(obs.player2).__name__ == "Player" and obs.mark == 2:
            pass
        else:
            obs = self.game_instance.play_step(obs)
            self.button_grid.handle_click(obs.last_button_id, obs.mark)
            return obs

    def show_valid_buttons(self, obs, config):
        valid_moves_with_last_row = []
        for col in range(config.columns):
            row_id = []
            for row in range(config.rows - 1, -1, -1):
                if obs.board[row * config.columns + col] == 0:
                    row_id = row * config.columns + col
                    break
            valid_moves_with_last_row.append(row_id)
        return  valid_moves_with_last_row
    
    def reset(self, obs, button=False):
        obs = self.game_instance.reset(obs, button)
        self.button_grid = buttons.ButtonGrid(rows=config.rows, cols=config.columns, button_radius=25, screen=self.screen, margin=10)
        return obs
        
    def return_to_main_menu(self):
        if self.aigames_instance:
            self.aigames_instance.run()
            
            
    def exit_game(self):
        self.running = False
        
    def automove(self):
        if self.pause:
            self.pause = False
        else: 
            self.pause = True
    


