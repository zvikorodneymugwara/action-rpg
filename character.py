import pygame

from healthbar import HealthBar
from actor import AnimatedActor

# all characters come from this class


class Character(AnimatedActor):
    def __init__(self, x: int, y: int, char_type: str, scale: float, health: int):
        super().__init__(x, y, char_type, scale)
        self.alive = True
        self.direction = pygame.math.Vector2()
        self.max_health = self.health = health
        self.health_bar = HealthBar(x, y, self.health, self.max_health)
        self.offset_placed = False
        self.attack_timer = 0

    def update(self, player, level_num: int):
        self.health_bar.x = self.rect.x
        return super().update(player, level_num)
