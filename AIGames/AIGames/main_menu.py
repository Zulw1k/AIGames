import pygame
import buttons
import sys
sys.path.append('C:/Users/Wojtek/source/repos/AIGames/AIGames/ConnectFour/')
from ConnectFour import connectFour, game



class AIGames:
    def __init__(self):
        pygame.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("AIGames")
        
        # Define fonts
        self.font = pygame.font.SysFont('arialblack', 40)
        
        # Game variables
        self.game_paused = False
        
        # Instances
        self.connfour = connectFour.ConnectFour(aigames_instance=self, game_instance=game.Game())
        
        # Text
        self.maintitle = buttons.Text(x=150, y=25, text="AIGames", font=self.font, screen=self.screen)
        
        # Buttons
        self.connectfour_button = buttons.Button(target_instance=self.connfour, target_method='start',
                                                 x=200, y=100, width=100, height=40, screen=self.screen, text="ConnectFour")
        self.exit_button = buttons.Button(target_instance=self, target_method='exit_game',
                                          x=200, y=150, width=100, height=40, screen=self.screen, text="Exit")
        

    def run(self):
        # Set up display
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("AIGames")
        # Game loop
        self.running = True
        while self.running:
            self.screen.fill((60, 70, 90))
            
            # Draw features on the screen
            self.maintitle.draw()
            self.connectfour_button.draw()
            self.exit_button.draw()
            
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        self.connectfour_button.handle_click(pos)
                        self.exit_button.handle_click(pos)
            
            pygame.display.update()

        pygame.quit()
        sys.exit()
        
    def exit_game(self):
        self.running = False

# Instantiate and run the game
if __name__ == "__main__":
    game = AIGames()
    game.run()




