import pygame

class Laser(pygame.sprite.Sprite):
    """Laser class inheriting from pygame.sprite.Sprite"""
    def __init__(self, screen_height: int, pos: tuple[int, int], speed: int = -8) -> None:
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self) -> None:
        """Destroy itself when goes out of bounds"""
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self) -> None:
        self.rect.y += self.speed
        self.destroy()