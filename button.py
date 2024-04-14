import pygame


class Button():
    """Creates button it takes in the x and y coordinates for
    the button's position. Draw detetcts when the button is clicked and draws the button on the screen """

    def __init__(self, x, y, font, text, col):
        self.font = font
        self.text = text
        self.image = self.font.render(self.text, True, 'white')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.active_col = 'red'
        self.col = col
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.image = self.font.render(self.text, True, self.active_col)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            self.image = self.font.render(self.text, True, self.col)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x-self.image.get_width() /
                     2, self.rect.y-self.image.get_height()/2))

        return action


# image button class
class ImageButton():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
