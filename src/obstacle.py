import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, size: int, color: tuple[int, int, int], x: int, y: int) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))


shape: list[str] = [
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx'
]