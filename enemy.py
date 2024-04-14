import pygame
from random import choice, randint

from character import Character
from settings import slash

# base class for all enemies


class Enemy(Character):
    def __init__(self, x: int, y: int, char_type: str, scale: float, health: int):
        super().__init__(x, y, char_type, scale, health)
        self.attack_rect = self.rect
        self.direction.x = choice([-1, 1])
        self.speed = randint(1, 2)
        self.original_spd = self.speed
        self.dmg = 5

    # updates position of the attack rect for the enemy
    def update_attack_rect(self):
        if not self.flip:
            self.attack_rect = pygame.Rect(
                self.rect.x, self.rect.y, self.image.get_width()*1.5, self.image.get_height())
        else:
            self.attack_rect = pygame.Rect(self.rect.x-self.image.get_width(
            )*0.5, self.rect.y, self.image.get_width()*1.5, self.image.get_height())

    # controlls how the enemy attacks the player
    def attack_player(self, player):
        if self.attack:
            self.state = 'attack'
        if self.attack_timer <= 0:
            player.health -= self.dmg
            slash.play()
            # enemy attacks and player loses health at the end of the animations
            self.attack_timer = len(
                self.animations['attack'])/self.animation_speed

    # flip the image accordingly
    def flip_image(self):
        if self.direction.x < 0:
            self.flip = True
        else:
            self.flip = False

    # the ai of the enemys, how they move and attack
    def ai(self, constraints: pygame.sprite.Group, player):

        self.rect.x += self.speed * self.direction.x  # movement

        # change direcitons when the enemy reaches a constraint
        for c in constraints:
            if c.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = c.rect.right
                if self.direction.x > 0:
                    self.rect.right = c.rect.left
                self.direction.x *= -1

        for p in player:
            # if the player is within attacking range, attack the player
            if p.rect.colliderect(self.attack_rect) and p.alive:
                # stop moving and attack the player
                self.attack = True
                self.speed = 0
                self.attack_timer -= 1
                self.attack_player(p)
            else:
                # else continue moving in your original direction
                self.attack = False
                self.speed = self.original_spd

        if not self.attack:
            self.attack_timer = len(
                self.animations['attack'])/self.animation_speed
            self.state = "move"

        if self.health <= 0:
            self.alive = False
            self.state = "death"

    def update(self, player, level_num: int, constraints: pygame.sprite.Group):
        self.flip_image()
        self.update_attack_rect()
        super().update(player, level_num)

# skeletons
# skeleton types determine the images loaded


class Skeleton(Enemy):
    def __init__(self, x: int, y: int, skeleton_type: int, scale: float):
        super().__init__(x, y, 'skeleton', scale, health=75)

        # images
        self.animations = {'attack': [], 'move': [], 'death': []}
        spacing = 0
        self.skeleton_type = skeleton_type
        self.steps = []
        self.healed = False
        '''
        each enemy has different sized images
        so each image and in some cases each animation requires
        a particular number of steps, image sizes and x,y coordinates
        for each animation indexed 1 to 3, these values are stored in lists
        '''
        if skeleton_type == 1:
            # attack move death
            rects = [pygame.Rect(0, 0, 43, 37),
                     pygame.Rect(0, 0, 22, 32),
                     pygame.Rect(0, 0, 33, 32)]
            self.steps = [18, 13, 15]
            spacing = [43, 22, 33]
        if skeleton_type == 2:
            rects = [pygame.Rect(0, 10, 64, 40),
                     pygame.Rect(0, 10, 55, 40),
                     pygame.Rect(0, 10, 55, 40)]
            self.steps = [13, 12, 13]
            spacing = [64, 64, 64]
        if skeleton_type == 3:
            rects = [pygame.Rect(0, 0, 48, 38),
                     pygame.Rect(0, 0, 48, 48),
                     pygame.Rect(0, 0, 72, 32)]
            self.steps = [20, 20, 13]
            spacing = [56, 56, 72]
        for count, animation in enumerate(self.animations):
            self.animations[animation] = self.load_images(
                f'{self.path}_{skeleton_type}/{animation}.png', rects[count], self.steps[count], spacing[count])
        self.state = 'move'
        self.image = self.animations[self.state][int(self.index)]
        if skeleton_type != 2:
            self.rect.y -= self.image.get_height()/2
        else:
            self.rect.y -= (self.image.get_height()/2+6)
        self.attack_rect = self.animations['attack'][0].get_rect(
            topleft=(x, y))
        self.rect = self.image.get_rect(topleft=(x, y))

    '''
    due to the differences in image sizes to what is scaled according to the tile size
    in the actor.py module, some image offsets are reqiured for things to look normal
    '''

    def place_image_offest(self):
        if self.skeleton_type == 1:
            if self.state == 'attack' and not self.offset_placed:
                self.rect.y -= 12
                self.offset_placed = True
            elif self.state != 'attack' and self.offset_placed:
                self.rect.y += 12
                self.offset_placed = False

        if self.skeleton_type == 3:
            if self.state == 'death' and not self.offset_placed:
                self.rect.y += 16
                self.offset_placed = True

    def update(self, player, level_num: int, constraints: pygame.sprite.Group):
        if self.alive:  # run ai if alive
            self.ai(constraints, player)
            if self.health > self.max_health:
                self.health = self.max_health
        self.place_image_offest()
        return super().update(player, level_num, constraints)
