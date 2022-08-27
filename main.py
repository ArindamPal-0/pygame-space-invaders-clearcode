import pygame, sys
from src.player import Player

class Game:
    def __init__(self, player_pos: tuple[int, int], screen_width: int) -> None:
        """initialize all the game objects"""
        player_sprite = Player("graphics/player.png", player_pos, screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

    def run(self, screen: pygame.Surface) -> None:
        """update and draw all sprite groups, will run every game loop"""
        self.player.update()
        self.player.draw(screen)

def main() -> int:
    # initializing pygame
    pygame.init()

    # screen width and height
    screen_width: int = 600
    screen_height: int = 600

    # creating a display surface
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # creating a game instance
    game = Game((screen_width / 2, screen_height), screen_width)

    while True:
        for event in pygame.event.get():
            # checking for exit event
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
        
        # giving a simple background color
        screen.fill((30, 30, 30))

        # running all the game draw and update logic
        game.run(screen)

        # displaying it on screen
        pygame.display.flip()

        # used to limit the framerate to 60 Hz
        clock.tick(60)

    return 0

if __name__ == "__main__":
    sys.exit(main())