# import modules used
import pygame

from button import ImageButton
from settings import *
from player import *
from level import Level

pygame.init()

# screen height, clock and fonts used in game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Times New Roman', 64)
font2 = pygame.font.SysFont('Times New Roman', 36)

# main game word, menu animation and pause button image
wrld = None
menu_anim = MenuAnimation(0, 0, 'menu_animation', 0.13, 256, 256)
victory_anim = MenuAnimation(0,0,'victory_animation', 0.1, 402, 403)
pause_image = pygame.image.load("assets/images/pause.png").convert_alpha()

# boolean statements used to control the game
start_game = False
display_menu = True
display_options = False
game_beaten = False
show_options = False
loaded = False
game_over = False
level_number = 2
run = True

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit
            run = False

    # draw the main menu if the game hasnt started
    if not start_game:
        screen.fill((82, 82, 82))
        menu_anim.draw(screen)
        menu_anim.update()

    # showing menu
    if display_menu:
        # show buttons
        for x in range(0, len(MENU_BTNS)):
            if Button(WIDTH*0.8, HEIGHT*0.3+(100*x), font, MENU_BTNS[x], 'black').draw(screen):
                menu_nav.play()  # menu button click audio effect
                if x == 0:  # start button
                    display_menu = False
                    start_game = True
                if x == 1:  # options button
                    show_options = True
                    display_menu = False
                if x == 2:  # exit button
                    run = False

    # if the game has started
    if start_game:
        # load the level
        if not loaded:
            wrld = Level(load_level(level_number), level_number)
            loaded = True
        else:
            # run the game
            for player in wrld.player:
                if player.next_level:  # load next level if the player is done
                    level_number += 1
                    loaded = False
                if player.alive is False:  # if the player is dead
                    game_over = True
                if player.victory:
                    game_beaten = True  #victory screen
            wrld.run(screen, font2)
            #pause button
            if ImageButton(WIDTH*0.93, HEIGHT*0.05, pause_image, 0.08).draw(screen):
                menu_nav.play()
                pause(clock, screen, Button(WIDTH/2, HEIGHT/2, font, 'RESUME', 'black'),
                      Button(WIDTH/2, HEIGHT*0.6, font, 'EXIT', 'black'), font)

    # if the player has died
    if game_over:
        start_game = False
        loaded = False
        buttons = []
        # show the death screen
        screen.fill('black')
        draw_text(WIDTH/2, HEIGHT*0.35, "YOU DIED!", font, screen, 'red')
        for count, btn in enumerate(MENU_BTNS_2):
            buttons.append(Button(WIDTH/2, HEIGHT*0.5+(100*count),
                           font, MENU_BTNS_2[count], 'white'))
        if buttons[0].draw(screen):  # restart level
            menu_nav.play()
            start_game = True
            game_over = False
        if buttons[1].draw(screen):  # exit
            menu_nav.play()
            run = False

    # if the player has beaten the game
    if game_beaten:
        screen.fill((139,139,139,255))
        victory_anim.draw(screen)
        victory_anim.update()
        start_game = False
        loaded = False
        draw_text(WIDTH*0.65, HEIGHT*0.3, "VICTORY!",font,screen,'gold')
        exit_btn = Button(WIDTH*0.65, HEIGHT/2, font, "EXIT", 'black')
        if exit_btn.draw(screen):  # exit
            menu_nav.play()
            run = False

    # options screen
    if show_options:
        draw_text(WIDTH*0.66, HEIGHT*0.3, 'VOLUME', font2, screen, 'black')
        pygame.draw.rect(screen, (37, 37, 37), pygame.Rect(
            WIDTH*0.6, HEIGHT*0.35, 160, 40))
        draw_text(WIDTH*0.69, HEIGHT*0.5, 'BRIGHTNESS', font2, screen, 'black')
        pygame.draw.rect(screen, (57, 57, 57), pygame.Rect(
            WIDTH*0.6, HEIGHT*0.55, 110, 40))
        if Button(WIDTH*0.65, HEIGHT*0.8, font, "BACK", "black").draw(screen):
            menu_nav.play()
            show_options = False
            display_menu = True
            
    pygame.display.update()
