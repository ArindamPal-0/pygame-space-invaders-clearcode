import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, path: str, color: str, x: int, y: int) -> None:
        super().__init__()
        file_path = f'{path}/{color}.png'
        self.image: pygame.Surface = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction) -> None:
        """Move the alien in x axis"""
        self.rect.x += direction


class Extra(pygame.sprite.Sprite):
    def __init__(self, path: str, side: str, screen_width: int) -> None:
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()

        if side == "right":
            x = screen_width + 50
            self.speed: int = -3
        else:
            x = -50
            self.speed: int = 3

        self.rect = self.image.get_rect(topleft = (x, 80))

    def update(self) -> None:
        self.rect.x += self.speed