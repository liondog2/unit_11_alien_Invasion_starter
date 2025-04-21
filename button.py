import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """
    Base class for a button UI element.

    Attributes:
        settings (Settings): The settings of the game and its' objects.
        font (pygame.font.Font): The font to be used on the button's text
    """
    def __init__(self, game: 'AlienInvasion', msg: str) -> None:
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        
        self.font = pygame.font.Font(
            self.settings.font_file, self.settings.HUD_font_size
        )
        self.rect = pygame.Rect(
            0, 0, self.settings.button_w, self.settings.button_h
        )
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)
    
    def _prep_msg(self, msg: str) -> None:
        """
        Render the font and create the rect.

        Params:
            msg (str): The message to be rendered as text.
        """
        self.msg_image = self.font.render(
            msg, True, self.settings.text_color, None
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw(self) -> None:
        """
        Draw the button to the screen and fill the rect with the button
        color and text.
        """
        self.screen.fill(
            self.settings.button_color, self.rect
        )
        self.screen.blit(self.msg_image, self.msg_image_rect)
    
    def check_clicked(self, mouse_pos: tuple) -> bool:
        """
        Called when left mouse input is detected. If the position of the
        mouse collides with the rect of the button, return True.

        Params:
            mouse_pos (tuple): The (x, y) position of the mouse.
        """
        return self.rect.collidepoint(mouse_pos)
