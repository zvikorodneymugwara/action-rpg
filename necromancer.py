# import all modules
import pygame
from random import randint

from enemy import *
from settings import import_csv_layout, TILE_SIZE, draw_text
from pathfinder import Pathfinder


class Necromancer(Enemy):
    def __init__(self, x: int, y: int, scale: float):
        super().__init__(x, y, 'necromancer', scale, health=150)

        # load the images
        # the animations of the necromancer and the steprs
        self.animations = {'death': [], 'heal': [], 'move': [], 'summon': []}
        steps = [9, 13, 8, 13]
        for count, animation in enumerate(self.animations):
            self.animations[animation] = self.load_images(
                f'{self.path}/{animation}.png', pygame.Rect(60, 60, 68, 68), steps[count], 160)
        self.skeletons = pygame.sprite.Group()
        self.state = 'move'
        self.image = self.animations[self.state][int(self.index)]

        # logic
        self.attack_rect = self.animations['move'][0].get_rect(topleft=(x, y))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.range_rect = pygame.Rect(0, 0, 0, 0)
        self.speed = 2
        self.old_path = []
        self.spawn_counter = 0
        self.text = ''
        self.heal_counter = 300
        self.spawning = False
        self.healing = False
        self.text_counter = 0

        # pathfinding
        self.grid = import_csv_layout(
            'assets/levels/level3/data/level3_floor.csv',)
        self.path_finder = Pathfinder(self.grid)
        self.path = []
        self.empty_path = []
        self.collision_rects = []
        self.pos = self.rect.center
        self.path_timer = 0

    # setting the path that the necromancer will follow to the player
    def set_path(self, path):
        self.old_path = self.path
        self.path = path
        self.create_collision_rects()
        self.get_direction()

    # calculates the direction of the necromancer when moving along path
    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    # checks collision with set points so as to change direction of the necromancer
    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.colliderect(self.rect):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.path = []

    # create the points where the necromacer must change directions
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] * TILE_SIZE) + TILE_SIZE//2
                y = (point[1] * TILE_SIZE) + TILE_SIZE//2
                rect = pygame.Rect((x - 2, y - 2), (TILE_SIZE, TILE_SIZE))
                self.collision_rects.append(rect)

    # necromancer ai
    def ai(self, player):
        self.heal_counter -= 1

        # fix range of enemy vision
        if self.flip:
            self.range_rect = pygame.Rect(
                self.rect.x-self.rect.width*2, self.rect.y, self.rect.width*3, self.rect.height)
        else:
            self.range_rect = pygame.Rect(
                self.rect.x, self.rect.y, self.rect.width*3, self.rect.height)

        for p in player:
            # summoning
            if p.rect.colliderect(self.range_rect):
                self.spawn_counter -= 1
                self.spawning = True
                if self.spawn_counter <= 0 and p.direction.y == 0:
                    y_pos = p.rect.y
                    skeleton_type = randint(1, 3)
                    if skeleton_type == 1:
                        y_pos += 16
                    else:
                        y_pos += 8
                    # exact position of skeleton based on the direction the necromancer is facing
                    if self.flip:
                        skeleton = Skeleton(
                            self.range_rect.left/2, y_pos, skeleton_type, TILE_SIZE/16)
                    else:
                        skeleton = Skeleton(
                            self.range_rect.right/2, y_pos, skeleton_type, TILE_SIZE/16)
                    self.skeletons.add(skeleton)
                    self.spawn_counter = 200
            else:
                self.spawining = False

        # healing
        if self.heal_counter <= 30:
            heal_amount = 0
            self.healing = True
            chance = randint(0, 100)
            # three levels of healing based on probability
            if chance <= 15:  # 15% chance of greater heal
                heal_amount = 60
                self.text = 'Greater Heal'
            elif 15 < chance <= 30:  # 30% chance of heal
                heal_amount = 30
                self.text = 'Heal'
            elif 30 < chance <= 60:  # 60% chance of lesser heal
                heal_amount = 10
                self.text = 'Lesser Heal'
            # heal if there is a skeleton available to heal or if health is low
            if len(self.skeletons) > 0:
                if self.health < self.max_health:
                    self.text_counter = 60
                for skeleton in self.skeletons:
                    if not skeleton.healed:
                        skeleton.health += heal_amount
                        skeleton.healed = True
            if self.health < self.max_health:
                self.health += heal_amount
            self.heal_counter = 300  # reset heal counter
        else:
            self.healing = False
            if len(self.skeletons) > 0:
                for skeleton in self.skeletons:
                    if skeleton.healed:
                        skeleton.healed = False

    def update(self, screen: pygame.Surface,  player, level_num: int,  constraints: pygame.sprite.Group):
        # run all logic if alive
        if self.alive:
            self.path_timer -= 1
            self.text_counter -= 1
            self.pos += self.direction*self.speed
            self.check_collisions()
            self.rect.center = self.pos
            self.ai(player)

            if self.health > self.max_health:
                self.health = self.max_health

            if self.text_counter > 0:
                draw_text(self.rect.centerx, self.rect.y-20, self.text, pygame.font.SysFont(
                    "Times New Roman", 16, 'bold'), screen, 'green')

            if self.path_timer <= 0:  # set a new path if the player moves when the timer hits 0
                self.set_path(self.path_finder.path)
                self.path_finder.update(
                    self.rect.centerx, self.rect.centery, player)
                self.path_timer = 120

            if self.text_counter <= 0:
                self.text_counter = 0

            if self.spawn_counter < 30 and self.spawning:
                self.state = 'summon'
            elif self.healing:
                self.state = 'heal'
            else:
                self.state = 'move'

            if self.health <= 0:
                self.health = 0
                self.alive = False

        else:
            self.state = 'death'

        self.skeletons.draw(screen)
        self.skeletons.update(player, 3, constraints)

        # player interactions with skeletons similar to that in the level class in the logic method
        for p in player:
            for enemy in self.skeletons:
                if enemy.alive:
                    enemy.health_bar.draw(
                        enemy.animations['move'][0].get_width(), enemy.health, screen)
                    enemy.health_bar.x = enemy.rect.left
                    enemy.health_bar.y = enemy.rect.top
                if enemy.alive and p.range_rect.colliderect(enemy.rect)\
                        and p.attack and p.take_target_hp:
                    enemy.health -= 40
                    slash.play()

        return super().update(player, level_num, constraints)
