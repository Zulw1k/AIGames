
import pygame
import sys
import math
sys.path.append('C:/Users/Wojtek/source/repos/AIGames/AIGames/ConnectFour/')
from ConnectFour import agents, obs

class Text:
    def __init__(self, x, y, text, screen, font, text_col=(255, 255, 255)):
        self.font = font
        self.text_col = text_col
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        
    def draw(self):
        img = self.font.render(self.text, True, self.text_col)
        self.screen.blit(img, (self.x, self.y))

class Button:
    def __init__(self,target_instance, target_method, x, y, width, height, screen, text, color=(255, 255, 255), text_color=(0, 0, 0), font_size=20, args=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.target_instance = target_instance
        self.target_method = target_method
        self.args = args

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos):
        if self.rect.collidepoint(pos) and self.target_instance and self.target_method:
            if self.args is not None:
                getattr(self.target_instance, self.target_method)(*self.args)
            else:
                getattr(self.target_instance, self.target_method)()
                
        
class ButtonGrid:
    def __init__(self, rows, cols, button_radius, screen, margin, start_pos=(20, 20)):
        self.rows = rows
        self.cols = cols
        self.button_radius = button_radius
        self.margin = margin
        self.screen = screen
        self.start_pos = start_pos
        self.buttons = []

        # Initialize buttons
        for row in range(rows):
            for col in range(cols):
                x = self.start_pos[0] + col * (2 * self.button_radius + margin) + self.button_radius + margin
                y = self.start_pos[1] + row * (2 * self.button_radius + margin) + self.button_radius + margin
                self.buttons.append({'pos': (x, y), 'id': row * cols + col, 'color': (255, 255, 255), 'clicked': False, 'border_color': (0, 0, 0)})
                
    def clear_buttons(self):
        self.buttons = []

    def draw(self):
        # Draw frame around the button grid
        grid_width = self.cols * (2 * self.button_radius + self.margin) - self.margin
        grid_height = self.rows * (2 * self.button_radius + self.margin) - self.margin
        pygame.draw.rect(self.screen, (0, 0, 0), (self.start_pos[0] + self.margin - self.button_radius, self.start_pos[1] + self.margin - self.button_radius,
                                           grid_width + 2 * self.button_radius, grid_height + 2 * self.button_radius), 2)

        # Draw buttons
        for button in self.buttons:
            pygame.draw.circle(self.screen, button['color'], button['pos'], self.button_radius)
            pygame.draw.circle(self.screen, button['border_color'], button['pos'], self.button_radius, 6)
            
    def show_valid_buttons(self, button_ids):
        for button in self.buttons:
            if button['id'] in button_ids:
                button['border_color'] = (0, 0, 255)
                button['clicked'] = False
            else:
                button['clicked'] = True
                button['border_color'] = (0, 0, 0)    
    
    def disable_buttons(self):
        for button in self.buttons:
            button['border_color'] = (0, 0, 0) 
            button['clicked'] = True
            
    def handle_click(self, arg, mark):
        if isinstance(arg, tuple):  # If arg is a position tuple (pos)
            pos = arg
            for button in self.buttons:
                distance = math.sqrt((pos[0] - button['pos'][0])**2 + (pos[1] - button['pos'][1])**2)
                if distance <= self.button_radius and not button['clicked']:
                    button['clicked'] = True
                    if mark == 1:
                        button['color'] = (255, 0, 0)  # Change the color to red (you can customize this)
                    else:
                        button['color'] = (255, 255, 0)  # Change the color to red (you can customize this)
                    return button['id']
        else:
            button_id = arg
            for button in self.buttons:
                if button['id'] == button_id:
                    button['clicked'] = True
                    if mark == 2:
                        button['color'] = (255, 0, 0)  # Change the color to red (you can customize this)
                    else:
                        button['color'] = (255, 255, 0)  # Change the color to red (you can customize this)
                    return button['id']
        return None
    
    def change_borders_to_blue(self, button_ids):
        for button in self.buttons:
            if button['id'] in button_ids:
                button['border_color'] = (0, 0, 255)
            else:
                button['border_color'] = (0, 0, 0)

        


class DropdownSelect:
    def __init__(self, x, y, width, height, options, screen, player, font_size=20, border_color=(0, 0, 0), border_width=2,
                 dropdown_color=(255, 255, 255), dropdown_selected_color=(200, 200, 200), text_color=(0, 0, 0),
                 scrollbar_color=(150, 150, 150), scrollbar_width=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.border_color = border_color
        self.border_width = border_width
        self.dropdown_color = dropdown_color
        self.dropdown_selected_color = dropdown_selected_color
        self.text_color = text_color
        self.scrollbar_color = scrollbar_color
        self.scrollbar_width = scrollbar_width
        self.is_open = False
        self.selected_option = self.options[0]
        self.scroll_offset = 0
        self.max_visible_options = min(2, len(self.options))  # Maximum number of options visible in the dropdown
        self.player = player

    def draw(self):
        pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width)

        # Draw selected option
        pygame.draw.rect(self.screen, self.dropdown_selected_color if self.is_open else self.dropdown_color, self.rect)
        text_surface = self.font.render(str(self.selected_option or ""), True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

        # Draw dropdown options if open
        if self.is_open:
            dropdown_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height,
                                        self.rect.width, self.max_visible_options * self.rect.height)
            pygame.draw.rect(self.screen, self.dropdown_color, dropdown_rect)

            # Draw scrollbar
            scrollbar_rect = pygame.Rect(self.rect.x + self.rect.width - self.scrollbar_width, dropdown_rect.y,
                                         self.scrollbar_width, dropdown_rect.height)
            pygame.draw.rect(self.screen, self.scrollbar_color, scrollbar_rect)

            # Calculate scrollbar position based on scroll_offset
            normalized_scroll_pos = (self.scroll_offset / (len(self.options) - self.max_visible_options))
            scrollbar_pos_y = dropdown_rect.y + normalized_scroll_pos * (dropdown_rect.height - self.scrollbar_width)

            # Draw the thumb of the scrollbar
            thumb_rect = pygame.Rect(scrollbar_rect.x, scrollbar_pos_y, scrollbar_rect.width, self.scrollbar_width)
            pygame.draw.rect(self.screen, (0, 0, 0), thumb_rect)

            for i in range(self.scroll_offset, min(len(self.options), self.scroll_offset + self.max_visible_options)):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i - self.scroll_offset + 1) * self.rect.height,
                                          self.rect.width - self.scrollbar_width, self.rect.height)
                pygame.draw.rect(self.screen, self.dropdown_selected_color if self.options[i] == self.selected_option else self.dropdown_color,
                                 option_rect)
                text_surface = self.font.render(str(self.options[i]), True, self.text_color)
                text_rect = text_surface.get_rect(center=option_rect.center)
                self.screen.blit(text_surface, text_rect)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.is_open = not self.is_open
        elif self.is_open:
            scrollbar_rect = pygame.Rect(self.rect.x + self.rect.width - self.scrollbar_width,
                                         self.rect.y + self.rect.height, self.scrollbar_width, self.max_visible_options * self.rect.height)
            if scrollbar_rect.collidepoint(pos):
                # Handle scrollbar click
                normalized_pos = pos[1] - scrollbar_rect.y
                normalized_pos = max(0, min(normalized_pos, scrollbar_rect.height - self.scrollbar_width))
                percentage = normalized_pos / (scrollbar_rect.height - self.scrollbar_width)
                self.scroll_offset = int((len(self.options) - self.max_visible_options) * percentage)
            else:
                for i in range(self.scroll_offset, min(len(self.options), self.scroll_offset + self.max_visible_options)):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i - self.scroll_offset + 1) * self.rect.height,
                                              self.rect.width - self.scrollbar_width, self.rect.height)
                    if option_rect.collidepoint(pos):
                        self.selected_option = self.options[i]
                        self.is_open = False
                        if self.player == 1:
                            obs.player1 = agents.agent_dict[self.options[i]]
                        else:
                            obs.player2 = agents.agent_dict[self.options[i]]