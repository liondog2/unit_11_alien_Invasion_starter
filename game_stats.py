class GameStats():
    """
    Track the status of the game.

    Attributes:
        ships_left (int): The number of ships the player has left.
    """
    def __init__(self, ship_limit: int) -> None:
        """
        Initialize GameStats with a set number of ships.

        Args:
            ship_limit (int): The initial number of ships available to the player.
        """
        self.ships_left = ship_limit