import pygame, sys
from src.player import Player
from src import obstacle

class Game:
    def __init__(self, player_pos: tuple[int, int], screen_width: int) -> None:
        """initialize all the game objects"""
        # Player setup
        player_sprite = Player("graphics/player.png", player_pos, screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # obstacle setup
        self.shape: list[str] = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount: int = 4
        self.obstacle_x_positions: list[int] = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions, x_start=40, y_start=480)

    def create_obstacle(self, x_start: int, y_start: int, offset_x: int):
        for row, row_value in enumerate(self.shape):
            for col, col_value in enumerate(row_value):
                if col_value == 'x':
                    x: int = x_start + col * self.block_size + offset_x
                    y: int = y_start + row * self.block_size
                    block: pygame.sprite.Sprite = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)
    
    def create_multiple_obstacle(self, *offset: int, x_start: int, y_start: int):
        for x in offset:
            self.create_obstacle(x_start, y_start, x)

    def run(self, screen: pygame.Surface) -> None:
        """update and draw all sprite groups, will run every game loop"""
        self.player.sprite.lasers.update()
        self.player.update()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)

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