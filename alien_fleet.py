import pygame
from typing import TYPE_CHECKING
from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_move_speed = self.settings.fleet_move_speed

        self.create_fleet()

    def create_fleet(self) -> None:
        # Alien size
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        # Screen size
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(
            alien_w, screen_w, alien_h, screen_h
        )

        x_offset, y_offset = self.calculate_offsets(
            alien_w, alien_h, fleet_w, fleet_h, screen_h
        )
        # Create the battalion
        self._create_rectangle_fleet(
            alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset
        )

    def _create_rectangle_fleet(
        self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset
    ) -> None:
        for col in range(fleet_w):
            for row in range(fleet_h):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if row % 2 == 0 or col % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(
        self, alien_w, alien_h, fleet_w, fleet_h, screen_h
    ) -> None:
        # half_screen = self.settings.screen_w//2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h

        x_offset = int(self.settings.screen_w-fleet_horizontal_space)
        y_offset = int((screen_h-fleet_vertical_space)//2)
        return x_offset,y_offset

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h) -> tuple:
        fleet_w = ((screen_w/2)//alien_w)
        fleet_h = (screen_h//alien_h)
        
        # Width
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2
        
        # Height
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2
        return int(fleet_w), int(fleet_h)
    
    def _create_alien(self, current_x: int, current_y: int) -> None:
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self) -> None:
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._move_alien_fleet()
                self.fleet_direction *= -1
                break

    def _move_alien_fleet(self) -> None:
        for alien in self.fleet:
            alien.x -= self.settings.fleet_move_speed

    def update_fleet(self) -> None:
        self._check_fleet_edges()
        self.fleet.update()
    
    def draw(self) -> None:
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()
    
    def check_collisions(self, other_group) -> None:
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_left(self) -> bool:
        alien: Alien
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False
    
    def check_destroyed_status(self) -> bool:
        return not self.fleet