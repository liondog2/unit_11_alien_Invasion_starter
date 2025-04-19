# from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """
    Track the status of the game.

    Attributes:
        ships_left (int): The number of ships the player has left.
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        """
        Initialize GameStats with a set number of ships.

        Args:
            game (AlienInvasion): The base game.

        Attributes:
            ship_limit (int): The number of ships remaining.
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self) -> None:
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()
            # Save the file

    def save_scores(self) -> None:
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File not found: {e.value}')

    def reset_stats(self) -> None:
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1
    
    def update(self, collisions) -> None:
        # Update score
        self._update_score(collisions)

        # Update max_score
        self._update_max_score()
        # Update hi_score
        self._update_hi_score()
        
    def _update_max_score(self) -> None:
        if self.score > self.max_score:
            self.max_score = self.score
        # print(f'Max: {self.max_score}')

    def _update_hi_score(self) -> None:
        if self.score > self.hi_score:
            self.hi_score = self.score
        # print(f'Hi: {self.hi_score}')

    def _update_score(self, collisions) -> None:
        for alien in collisions.values():
            self.score += self.settings.alien_points
        # print(f'Basic: {self.score}')

    def update_level(self) -> None:
        self.level += 1
        # print(self.level)