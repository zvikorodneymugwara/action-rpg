# import modules
import pygame
import os

TILE_SIZE = 30  # all elements will be sized according to this

# all elements on screen originate from this class
class Actor(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=(x, y))

    def scroll(self, player, level_num: int):
        # change x coordinate of object based on player position
        if level_num < 3:
            if player.rect.right >= 700 and player.direction.x > 0:
                player.speed = 0
                self.rect.x -= 4
            elif player.rect.left <= 400 and player.direction.x < 0:
                player.speed = 0
                self.rect.x += 4
            else:
                player.speed = 4

    def update(self, player, level_num: int):
        for p in player:
            self.scroll(p, level_num)

# non animating actors will be of this class such as the ground or decor
class StaticActor(Actor):
    def __init__(self, x: int, y: int, image: pygame.Surface, scale: float):
        super().__init__(x, y)
        # load and set the image
        self.image = pygame.transform.scale(
            image, (image.get_width()*scale, image.get_height()*scale))
        self.rect = self.image.get_rect(topleft=(x, y))

# animating actors will be of this class such as enemies and coins
class AnimatedActor(Actor):
    def __init__(self, x: int, y: int, actor_type: str, scale: float):
        super().__init__(x, y)
        self.index = 0
        self.animation_speed = 0.16
        self.path = f'assets/images/{actor_type}'  # get the path of the images
        # all animations and images will be stored here
        self.animations = {'': []}
        self.flip = False
        self.state = ''
        self.scale = scale

    # images will be loaded here and returned in a list
    '''
    the image will be a subsurface of the original
    the path will be used to load the original uncut image
    the rect gets a rectagular selection of the image subsurface
    steps is how many frames of the image will be loaded
    spacing is the space between each frame
    '''
    def load_images(self, path: str, rect: pygame.Rect, steps: int, spacing: int):
        images = []
        img = pygame.image.load(path).convert_alpha()
        for x in range(0, steps):
            image = img.subsurface(
                rect.x+spacing*x, rect.y, rect.width, rect.height)
            image = pygame.transform.scale(
                image, (image.get_width()*self.scale, image.get_height()*self.scale))
            images.append(image)
        return images

    # animate method
    def animate(self):
        self.index += self.animation_speed
        if self.index > len(self.animations[self.state]):
            if self.state != "death":
                self.index = 0
            else:
                self.index = len(self.animations[self.state])-1

        self.image = pygame.transform.flip(
            self.animations[self.state][int(self.index)], self.flip, False)

    # update
    def update(self, player, level_num: int):
        self.animate()
        super().update(player, level_num)

    # draw
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


'''
Menu animation is a simple animated actor that required its own way of loading the images
'''
class MenuAnimation(AnimatedActor):
    def __init__(self, x: int, y: int, animation_type: str, delay: float, width: int, height: int):
        super().__init__(x, y, animation_type, 1)
        self.animations[animation_type] = []
        self.state = animation_type
        for x in range(0, len(os.listdir(self.path))):
            if x < 10:
                img = self.load_images(
                    rf'assets\images\{animation_type}\frame_0{x}_delay-{delay}s.png', pygame.Rect(0, 0, width, height), 1, 0)
            else:
                img = self.load_images(

                    rf'assets\images\{animation_type}\frame_{x}_delay-{delay}s.png', pygame.Rect(0, 0, width, height), 1, 0)
            if animation_type == "pause_animation":
                img[0] = pygame.transform.scale(img[0], (1280, 720))
            else:
                img[0] = pygame.transform.scale(img[0], (720, 720))

            self.animations[animation_type].append(img[0])

    # only need to animate the images
    def update(self):
        self.animate()

# coin is basic as well
class Coin(AnimatedActor):
    def __init__(self, x, y):
        super().__init__(x, y, 'coin', 1)
        self.animations['coin'] = self.load_images(
            f"{self.path}.png", pygame.Rect(0, 0, 16, 16), 4, 16)
        self.state = 'coin'
