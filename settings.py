# import modules
import pygame
from csv import reader
from pygame import mixer

from button import Button
from actor import TILE_SIZE, MenuAnimation

mixer.init()

WIDTH, HEIGHT = 1280, 23*TILE_SIZE  # window size
FPS = 60
MENU_BTNS = ['Start Game', 'Options', 'Exit']
MENU_BTNS_2 = ['Restart Level', 'Exit Game']

# load all the level data
def load_level(lvl_num: int):
    files = ['boss', 'bg', 'constraints', 'decor', 'end', 'health',
             'floor', 'spikes', 'spawn', 'foliage', 'coins', 'enemies']
    level = {}
    for f in files:
        path = f'assets/levels/level{lvl_num}/data/level{lvl_num}_{f}.csv'
        level[f] = path
    return level


# volumes
fx_vol = 0.2
music_vol = 0.25

# audio fx
menu_nav = pygame.mixer.Sound('assets/audio/menu_nav.wav')
game_over = pygame.mixer.Sound('assets/audio/game_over.wav')
jump = pygame.mixer.Sound('assets/audio/jump.wav')
victory_sound = pygame.mixer.Sound('assets/audio/win.wav')
game_over = pygame.mixer.Sound('assets/audio/game_over.wav')
pick_up = pygame.mixer.Sound('assets/audio/pick up.wav')
pick_up_2 = pygame.mixer.Sound('assets/audio/pick up 2.wav')
slash = pygame.mixer.Sound('assets/audio/slash.wav')

# music
pygame.mixer.music.load('assets/audio/music.wav')
pygame.mixer.music.set_volume(music_vol)
pygame.mixer.music.play(-1, 0, 2000)

# set the volumes
menu_nav.set_volume(fx_vol)
game_over.set_volume(fx_vol)
jump.set_volume(fx_vol*2)
victory_sound.set_volume(fx_vol)
game_over.set_volume(fx_vol)
pick_up.set_volume(fx_vol)
pick_up_2.set_volume(fx_vol)
slash.set_volume(fx_vol)

# get the csv file
def import_csv_layout(path: str):
    terrain_map = []
    with open(path) as level_map:
        level = reader(level_map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map

# generates a list of tiles cut from an orignal image similar to what was in the AnimatedActor class
def generate_cut_images(path: str):
    images = []
    img = pygame.image.load(path).convert_alpha()
    for x in range(0, int(img.get_height()/16)):
        for y in range(0, int(img.get_width()/16)):
            image = img.subsurface(pygame.Rect(y*16, x*16, 16, 16))
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            images.append(image)
    return images

# draw the text on screen
def draw_text(x: float, y: float, text: str, font: pygame.font.Font, screen: pygame.Surface, colour: str):
    img = font.render(text, True, colour)
    screen.blit(img, (x-img.get_width()/2, y-img.get_height()/2))


'''
run a second instance of pygame to pause the current one
'''
def pause(clock: pygame.time.Clock, screen: pygame.Surface, resume_btn: Button, exit_btn: Button, font: pygame.font.Font):
    paused = True
    paused_animation = MenuAnimation(0, 0, 'pause_animation', 0.11, 768, 384)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        paused_animation.draw(screen)
        paused_animation.update()
        draw_text(WIDTH*0.5, HEIGHT*0.33, "PAUSED", font, screen, 'red')
        if resume_btn.draw(screen):
            paused = False
        if exit_btn.draw(screen):
            paused = False
            pygame.quit()
            quit()

        clock.tick(60)
        pygame.display.update()
