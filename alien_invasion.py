import sys
import pygame

WINDOW_SIZE = (1200, 800)
class AlienInvasion:

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Alien Invasion")

        self.running = True

    def run_game(self) -> None:
        # Game Loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()