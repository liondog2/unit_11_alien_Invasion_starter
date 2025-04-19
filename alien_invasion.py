import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
# from alien import Alien
from alien_fleet import AlienFleet
from time import sleep
from button import Button
from hud import HUD

import random

class AlienInvasion:
    """
    Game manager for alien invasion.

    Attributes:
        settings (Settings): The settings of the game and its' objects.
        game_stats (GameStats): Manager for the stats of the game as it runs.
        bg (Surface): The background image.
        game_active (bool): If the game is currently running.
        running (bool): If the program is currently open.
        clock (Clock): Game clock.
    """
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)
        
        # Background
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_w, self.settings.screen_h)
            )
        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        
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

        self.play_button = Button(self, 'Play')
        self.game_active = False

    def run_game(self) -> None:
        # Game Loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()

            self.clock.tick(self.settings.FPS)

    def _check_collisions(self) -> None:
        # Check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            # Subtract one life if possible
            
        # Check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_right():
            self._check_game_status()
        # Check collisions of projectiles and aliens
        collisions = self.alien_fleet.check_collisions(
            self.ship.arsenal.arsenal
        )
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(450)
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            # Update GameStats level
            self.game_stats.update_level()
            # Update HUD view

    def _check_game_status(self) -> None:
        """
        If the number of ships left is greater than zero, subtract a life and
        reset the game. Otherwise, end the game by setting self.game_active to
        false.
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(.5)
        else:
            self.game_active = False
    
    def _reset_level(self) -> None:
        """
        Clear the arsenal. Remove the fleet and create a new one.
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self) -> None:
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self) -> None:
        """
        Draw the background, ship, and fleet. Flip the display.
        """
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)
        pygame.display.flip()

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()
    
    def _check_keyup_events(self, event) -> None:
        """
        Change movement state based on key releases
        """
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_up = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_down = False

    def _check_keydown_events(self, event) -> None:
        """
        Change movement state and actions based on key presses.
        """
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
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()