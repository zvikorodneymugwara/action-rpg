import pygame

#healthbar will change in length based on ratio of hp and max_hp
class HealthBar:
    def __init__(self, x:int, y:int, hp:int, max_hp:int):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self,length:int, hp:int, surface:pygame.Surface):
        # draw green health bar over red. green health bar varies with the ratio of max_health and current health
        self.hp = hp
        ratio = self.hp/self.max_hp
        # draw black border first
        pygame.draw.rect(surface, 'red', (self.x, self.y, length, 5))
        pygame.draw.rect(surface, 'green', (self.x, self.y, length * ratio, 5))


class EnemyHealth(HealthBar):
    def __init__(self, x:int, y:int, hp:int, max_hp:int):
        super().__init__(x, y, hp, max_hp)

    def draw(self, hp:int, len:int, surface:pygame.Surface):
        self.hp = hp
        ratio = self.hp/self.max_hp
        pygame.draw.rect(surface, 'red', (self.x, self.y, len, 5))
        pygame.draw.rect(surface, 'green', (self.x, self.y, len * ratio, 5))