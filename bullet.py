import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """
    A class to manage a single bullet fired from the player's ship.

    Inherits from:
        pygame.sprite.Sprite
    
    Attributes:
        screen (pygame.surface.Surface): The surface on which the bullet is 
        drawn.
        settings (Settings): The game settings.
        image (pygame.surface.Surface): The texture of the bullet.
        rect (pygame.surface.Surface): The position and dimensions of the bullet.
        x (float): the horizontal position of the bullet on the screen.
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.bullet_w, self.settings.bullet_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midright = game.ship.rect.midright
        self.x = float(self.rect.x)

    def update(self) -> None:
        """
        Move the bullet towards the left of the screen each frame at 
        bullet_speed. Update the rect.
        """
        self.x -= self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self) -> None:
        """
        Draw the bullet on the rect surface.
        """
        self.screen.blit(self.image, self.rect)