import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
# from alien import Alien
from alien_fleet import AlienFleet

import random

class AlienInvasion:

    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)
        
        # Background
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_w, self.settings.screen_h)
            )
        
        # Loop
        self.running = True
        self.clock = pygame.time.Clock()

        # Sound mixer
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(.5)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(.5)

        # Ship
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

    def run_game(self) -> None:
        # Game Loop
        while self.running:
            self._check_events()
            self.ship.update()
            self.alien_fleet.update_fleet()
            self._check_collisions()
            self._update_screen()

            self.clock.tick(self.settings.FPS)

    def _check_collisions(self) -> None:
        # Check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._reset_level()
            # Subtract one life if possible
            
        # Check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_left():
            self._reset_level()
        # Check collisions of projectiles and aliens
        collisions = self.alien_fleet.check_collisions(
            self.ship.arsenal.arsenal
        )
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(450)

    
    def _reset_level(self) -> None:
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def _update_screen(self) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        pygame.display.flip()

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keyup_events(self, event) -> None:
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_up = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_down = False

    def _check_keydown_events(self, event) -> None:
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_up = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(random.randint(150,400))
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()