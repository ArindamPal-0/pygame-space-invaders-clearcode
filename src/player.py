import pygame

class Player(pygame.sprite.Sprite):
    """Player class inheriting from pygame.sprite.Sprite"""
    def __init__(self, image_path: str, pos: tuple[int, int], constraint: int, speed: int) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(midbottom = pos)
        self.speed: int = speed
        self.max_x_constraint: int = constraint
    
        # adding delay to laser to prevent continuous shots
        self.ready: bool = True
        self.laser_time: int = 0
        self.laser_cooldown: int = 600

    def get_input(self) -> None:
        """getting player input"""
        keys =  pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            # time elapsed since the game has started
            self.laser_time = pygame.time.get_ticks()

    def recharge(self) -> None:
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self) -> None:
        """Keep the player character within screen bounds"""
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        print('shoot laser')

    def update(self) -> None:
        """Includes all the update logic of the player"""
        self.get_input()
        self.constraint()
        self.recharge()

        
