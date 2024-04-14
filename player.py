# import modules
import pygame
import os

from character import Character
from actor import StaticActor
from settings import jump, game_over

# player class


class Player(Character):
    def __init__(self, x: int, y: int, scale: float):
        super().__init__(x, y, "player", scale, health=100)  # initialize constructor
        # animations and images
        self.animations = {'attack': [], 'idle': [],
                           'jump': [], 'fall': [], 'run': []}
        for animation in self.animations:
            for x in range(0, len(os.listdir(f"{self.path}/{animation}"))):
                if animation == 'attack':
                    img = self.load_images(
                        f'{self.path}/{animation}/tile00{x}.png', pygame.Rect(50, 10, 64, 54), 1, 0)
                else:
                    img = self.load_images(
                        f'{self.path}/{animation}/tile00{x}.png', pygame.Rect(50, 10, 30, 54), 1, 0)
                self.animations[animation].append(img[0])
        self.state = 'idle'
        self.image = self.animations[self.state][int(self.index)]
        self.rect = self.image.get_rect(topleft=(x, y))

        # movement
        self.in_air = False
        self.on_ground = True
        self.speed = 4
        self.gravity = 1
        self.jump_height = -22

        # logic
        self.next_level = False
        self.score = 0
        self.attack = False
        self.victory = False
        self.attack_timer = 0
        self.take_hp = True
        self.range_rect = self.animations['attack'][0].get_rect(
            topleft=(x, y))

    # player controls
    def controls(self):
        keys = pygame.key.get_pressed()
        # jump if on the ground
        if keys[pygame.K_w] and self.in_air is False:
            self.direction.y = self.jump_height
            if self.direction.y < 0:
                self.in_air = True
                self.state = 'jump'
                jump.play()  # jump fx
                self.on_ground = False
        if self.alive:
            # move left
            if keys[pygame.K_a] and self.rect.left > 0:
                self.direction.x = -1
                if self.direction.y == 0:
                    self.state = 'run'
            # move right
            elif keys[pygame.K_d] and self.rect.right < 1280:
                self.direction.x = 1
                if self.direction.y == 0:
                    self.state = 'run'
            # attack
            elif keys[pygame.K_SPACE]:
                self.attack = True
                self.direction.x = 0
            else:  # else leave in idle
                self.direction.x = 0
                if self.direction.y == 0:
                    self.state = 'idle'
        else:  # if not alive, then dead
            self.state = "death"
            self.direction.x = 0

    # controls the attack of the player
    def update_attack(self):
        if self.attack and self.attack_timer >= 0:
            self.direction.x = 0
            self.attack_timer -= 1
            self.state = 'attack'

        # offset image
        if not self.offset_placed and self.flip and self.attack:
            self.rect.x -= 34
            self.offset_placed = True
        if self.offset_placed and not self.attack:
            self.rect.x += 34
            self.offset_placed = False

        # reset the attack timer
        if self.attack_timer <= 0:
            self.attack_timer = len(
                self.animations['attack'])/self.animation_speed
            self.attack = False

    # gravity on the player
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

        if self.on_ground:
            self.in_air = False

    # vertical collision with the world
    def vertical_movement(self, tiles: pygame.sprite.Group):
        self.apply_gravity()
        for tile in tiles:
            if type(tile) == StaticActor:
                if tile.rect.colliderect(self.rect):
                    if self.direction.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.direction.y = 0
                    if self.direction.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.direction.y = 0
                        self.on_ground = True

    # horizontal movement and collision with the world
    def horizontal_movement(self, tiles: pygame.sprite.Group):
        self.rect.x += self.speed * self.direction.x
        for tile in tiles:
            if type(tile) == StaticActor:
                if tile.rect.colliderect(self.rect):
                    if self.direction.x < 0:
                        self.rect.left = tile.rect.right
                    if self.direction.x > 0:
                        self.rect.right = tile.rect.left

    def update(self, tiles: pygame.sprite.Group):
        self.animate()
        self.controls()
        self.horizontal_movement(tiles)
        self.vertical_movement(tiles)
        self.update_attack()
        self.health_bar.x = self.rect.x
        self.health_bar.y = self.rect.top

        # flipping the image
        if self.direction.x < 0:
            self.flip = True
        elif self.direction.x > 0:
            self.flip = False

        if self.direction.y > 0:
            self.state = 'fall'

        if self.health <= 0:
            self.alive = False
            game_over.play()  # game over fx

        # periodically take target hp when attacking
        if self.attack and int(self.attack_timer) == 10:
            self.take_target_hp = True
        else:
            self.take_target_hp = False

        self.range_rect.x, self.range_rect.y = self.rect.x, self.rect.y
