import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        # Ship
        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        
        self.rect = self.image.get_rect()
        self._center_ship()
        
        # Flags
        self.moving_up = False
        self.moving_down = False

        self.arsenal = arsenal

    def _center_ship(self) -> None:
        """
        Reposition the ship at the mid right boundary of the screen.
        Set the y position to the rect's value on the y axis.
        """
        self.rect.midright = self.boundaries.midright
        self.y = float(self.rect.y)

    def update(self) -> None:
        # Updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        temp_speed = self.settings.ship_speed
        
        if self.moving_up and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
        if self.moving_down and self.rect.top > self.boundaries.top:
            self.y -= temp_speed
        
        self.rect.y = self.y

    def draw(self) -> None:
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self) -> bool:
        """Fire the bullet. Return a boolean if successful.
        
        Returns:
            bool: Whether or not the bullet fired successfully.
        """
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group) -> bool:
        """
        Check for collision on the ship from other_group. If spritecollideany
        returns true, center the ship and return true. Otherwise, return false.

        Args:
            other_group (Group): The other sprite group that will collide with
            the ship.

        Returns:
            bool: If a collision was detected.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False