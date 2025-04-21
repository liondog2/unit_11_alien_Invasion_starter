import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """
    A class to manage every bullet fired in the game, checking if any move out
    of bounds and if the amount on screen is less than the max amount of bullets
    that can be shot at once.

    Attributes:
        arsenal (pygame.sprite.Group): The sprite group for each bullet.
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self) -> None:
        self.arsenal.update()
        self._remove_bullets_offscreen()
    
    def _remove_bullets_offscreen(self) -> None:
        """For each bullet in an isolated copy of the table, check if the right
        bound of the bullet rect is less/equal to zero. If so, then it's off the 
        screen and it can be removed from arsenal.
        """
        for bullet in self.arsenal.copy():
            if bullet.rect.right <= 0:
                self.arsenal.remove(bullet)

    def draw(self) -> None:
        """For each bullet in the arsenal, call the draw_bullet() method of the
        bullet instance.
        """
        for bullet in self.arsenal:
            bullet.draw_bullet()
    
    def fire_bullet(self) -> bool:
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False