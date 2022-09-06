from asyncore import loop
import pygame, sys
from src.player import Player
from src import obstacle
from src.alien import Alien, Extra
import random
from src.laser import Laser

class Game:
    def __init__(self, player_pos: tuple[int, int], screen_width: int) -> None:
        """initialize all the game objects"""
        self.game_over = False

        # Audio
        music = pygame.mixer.Sound("audio/music.wav")
        music.set_volume(0.02)
        music.play(loops=-1)

        self.laserSound = pygame.mixer.Sound("audio/laser.wav")
        self.laserSound.set_volume(0.02)

        self.explosionSound = pygame.mixer.Sound("audio/explosion.wav")
        self.explosionSound.set_volume(0.08)

        # Player setup
        player_sprite = Player("graphics/player.png", self.laserSound, player_pos, screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 3
        self.lives_surface: pygame.Surface = pygame.image.load("graphics/player.png").convert_alpha()
        self.lives_x_start_pos: int = screen_width - (self.lives_surface.get_size()[0] * 2 + 20)

        self.score: int = 0
        self.font = pygame.font.Font("font/Pixeled.ttf", 20)

        # obstacle setup
        self.shape: list[str] = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount: int = 4
        self.obstacle_x_positions: list[int] = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions, x_start=40, y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(6, 8)
        self.alien_direction = 1

        # Extra Alien setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = random.randint(400, 800)


    def create_obstacle(self, x_start: int, y_start: int, offset_x: int) -> None:
        for row, row_value in enumerate(self.shape):
            for col, col_value in enumerate(row_value):
                if col_value == 'x':
                    x: int = x_start + col * self.block_size + offset_x
                    y: int = y_start + row * self.block_size
                    block: pygame.sprite.Sprite = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)
    
    def create_multiple_obstacle(self, *offset: int, x_start: int, y_start: int) -> None:
        for x in offset:
            self.create_obstacle(x_start, y_start, x)
    
    def alien_setup(self, rows: int, cols: int, x_distance: int = 60, y_distance: int = 48, x_offset: int = 70, y_offset: int = 100) -> None:
        for row in range(rows):
            for col in range(cols):
                x: int = col * x_distance + x_offset
                y: int = row * y_distance + y_offset

                if row == 0:
                    alien_sprite = Alien('graphics', 'yellow', x, y)
                elif 1 <= row <= 2: 
                    alien_sprite = Alien('graphics', 'green', x, y)
                else:
                    alien_sprite = Alien('graphics', 'red', x, y)

                self.aliens.add(alien_sprite)

    def alien_position_checker(self, screen_width: int) -> None:
        all_aliens: list[Alien] = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right > screen_width or alien.rect.left < 0:
                self.alien_direction = - self.alien_direction
                self.alien_move_down(2)
                break

    def alien_move_down(self, distance: int) -> None:
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self, screen_height: int) -> None:
        if self.aliens.sprites():
            random_alien: Alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(screen_height, random_alien.rect.midtop, 6)
            self.alien_lasers.add(laser_sprite)
            self.laserSound.play()

    def extra_alien_timer(self, screen_width: int) -> None:
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra("./graphics/extra.png", random.choice(["right", "left"]), screen_width))
            self.extra_spawn_time = random.randint(400, 800)


    def collision_checks(self):
        # player lasers
        for laser in self.player.sprite.lasers:
            # obstacle collisiosn
            if pygame.sprite.spritecollide(laser, self.blocks, True):
                laser.kill()

            # alien collisions
            aliens_hit: list[Alien] = pygame.sprite.spritecollide(laser, self.aliens, True)
            if aliens_hit:
                for alien in aliens_hit:
                    self.score += alien.value
                laser.kill()
                self.explosionSound.play()

            # extra collisions
            if pygame.sprite.spritecollide(laser, self.extra, True):
                laser.kill()
                self.score += 500
                self.explosionSound.play()

        # alien lasers
        for laser in self.alien_lasers:
            # obstacle collisiosn
            if pygame.sprite.spritecollide(laser, self.blocks, True):
                laser.kill()

            # player collision
            if pygame.sprite.spritecollide(laser, self.player, False):
                laser.kill()
                # print('hit')
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True

        # aliens
        for alien in self.aliens:
            # destroy obstacle on collision
            pygame.sprite.spritecollide(alien, self.blocks, True)

            if pygame.sprite.spritecollide(alien, self.player, False):
                self.game_over = True


    def display_lives(self, screen: pygame.Surface) -> None:
        for life in range(self.lives - 1):
            x: int = self.lives_x_start_pos + (life * (self.lives_surface.get_size()[0] + 10))
            screen.blit(self.lives_surface, (x, 8))


    def display_score(self, screen: pygame.Surface) -> None:
        score_surface: pygame.Surface = self.font.render(f"score: {self.score}", False, 'white')
        score_rect: pygame.Rect = score_surface.get_rect(topleft = (10, -10))
        screen.blit(score_surface, score_rect)


    def victory_message(self, screen: pygame.Surface) -> None:
        if not self.aliens.sprites():
            victory_surface: pygame.Surface = self.font.render("YOU WON", False, 'white')
            victory_rect: pygame.Rect =  victory_surface.get_rect(center=(screen.get_size()[0] / 2, screen.get_size()[1] / 2))
            screen.blit(victory_surface, victory_rect)


    def run(self, screen: pygame.Surface) -> bool:
        """update and draw all sprite groups, will run every game loop"""
        self.player.update()
        self.player.sprite.lasers.update()
        self.extra.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()

        self.alien_position_checker(screen.get_rect().right)
        self.extra_alien_timer(screen.get_rect().right)
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives(screen)
        self.display_score(screen)
        self.victory_message(screen)

        return self.game_over


class CRT:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.tv: pygame.Surface = pygame.image.load("graphics/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def create_crt_lines(self, screen_width: int, screen_height: int) -> None:
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos: int = line * line_height
            pygame.draw.line(self.tv, "black", (0, y_pos), (screen_width, y_pos), 1)

    def draw(self, screen: pygame.Surface) -> None:
        self.tv.set_alpha(random.randint(75, 90))
        self.create_crt_lines(*screen.get_size())
        screen.blit(self.tv, (0, 0))


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
    crt = CRT(screen_width, screen_height)

    # alien shoot event timer
    ALIEN_LASER: int = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIEN_LASER, 800)

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            # checking for exit event
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            if event.type == ALIEN_LASER:
                game.alien_shoot(screen_height)
        
        # giving a simple background color
        screen.fill((30, 30, 30))

        # running all the game draw and update logic
        game_over = game.run(screen)
        crt.draw(screen)

        # displaying it on screen
        pygame.display.flip()

        # used to limit the framerate to 60 Hz
        clock.tick(60)

        if game_over:
            pygame.quit()

    return 0

if __name__ == "__main__":
    sys.exit(main())