# modules used
import pygame

from settings import *
from player import Player
from enemy import *
from actor import *
from necromancer import *


class Level():
    def __init__(self, level_data: dict, level_number: int):
        self.level_number = level_number  # level number
        self.enemy_felled = False
        self.boss_felled = False

        # load background images based on the level
        if self.level_number < 3:
            self.bg_img1 = pygame.image.load(
                f'assets/levels/level{self.level_number}/Background_1.png').convert_alpha()
            self.bg_img2 = pygame.image.load(
                f'assets/levels/level{self.level_number}/Background_2.png').convert_alpha()
            # resize the background images accordingly
            if self.level_number == 1:
                self.bg_img1 = pygame.transform.scale(
                    self.bg_img1, (WIDTH, self.bg_img1.get_height()*2.6))
                self.bg_img2 = pygame.transform.scale(
                    self.bg_img2, (WIDTH, self.bg_img2.get_height()*2.6))
            else:
                self.bg_img1 = pygame.transform.scale(
                    self.bg_img1, (WIDTH, HEIGHT))
                self.bg_img2 = pygame.transform.scale(
                    self.bg_img2, (WIDTH, HEIGHT))

        # controlls the amount of times player health gets taken when on spikes
        self.spike_timer = 0

        # elements in their own sprite group
        # data is extracted from level_data dictionary in csv files
        boss_sprites = import_csv_layout(level_data['boss'])
        self.boss_sprites = self.create_tile_group(boss_sprites, 'boss')

        bg_sprites = import_csv_layout(level_data['bg'])
        self.bg_sprites = self.create_tile_group(bg_sprites, 'bg')

        constraints = import_csv_layout(level_data['constraints'])
        self.constraints = self.create_tile_group(constraints, 'constraints')

        decor_sprites = import_csv_layout(level_data['decor'])
        self.decor_sprites = self.create_tile_group(decor_sprites, 'decor')

        end_sprites = import_csv_layout(level_data['end'])
        self.end_sprites = self.create_tile_group(end_sprites, 'end')

        health_sprites = import_csv_layout(level_data['health'])
        self.health_sprites = self.create_tile_group(health_sprites, 'health')

        floor_sprites = import_csv_layout(level_data['floor'])
        self.floor_sprites = self.create_tile_group(floor_sprites, 'floor')

        spikes_sprites = import_csv_layout(level_data['spikes'])
        self.spikes_sprites = self.create_tile_group(spikes_sprites, 'spikes')

        coins_sprites = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_sprites, 'coins')

        foliage_sprites = import_csv_layout(level_data['foliage'])
        self.foliage_sprites = self.create_tile_group(
            foliage_sprites, 'foliage')

        enemies_sprites = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(
            enemies_sprites, 'enemies')

        # player
        start_pos = import_csv_layout(level_data['spawn'])
        self.player = self.create_tile_group(start_pos, 'spawn')

    def create_tile_group(self, layout, type: str):
        sprite_group = pygame.sprite.Group()  # group to return

        # level tiles are cut and stored
        images = generate_cut_images(
            f'assets/levels/level{self.level_number}/Assets.png')

        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':  # -1 is empty space. Any other value means something must be there
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    if type == 'coins':  # load the coins sprites
                        sprite_group.add(Coin(x, y))
                    if type == "boss":  # load the boss sprites
                        sprite = Necromancer(
                            x, HEIGHT-5*TILE_SIZE, 1.5*int(TILE_SIZE/16))
                        sprite_group.add(sprite)
                    if type == "bg":  # load the bg sprites
                        sprite_group.add(StaticActor(
                            x, y, images[int(value)], int(TILE_SIZE/16)))
                    if type == "constraints":  # load the constraints sprites
                        sprite_group.add(Actor(x, y))
                    if type == "decor":  # load the decor sprites
                        sprite_group.add(StaticActor(
                            x, y, images[int(value)], int(TILE_SIZE/16)))
                    if type == "end":  # load the end sprites
                        sprite_group.add(StaticActor(x-30, y-20, pygame.image.load(
                            'assets/levels/common/sign.png').convert_alpha(), 0.03))
                    if type == "health":  # load the health sprites
                        sprite_group.add(StaticActor(x-20, y, pygame.image.load(
                            'assets/levels/common/health.png').convert_alpha(), 0.08))
                    if type == "floor":  # load the floor sprites
                        sprite_group.add(StaticActor(
                            x, y, images[int(value)], int(TILE_SIZE/16)))
                    if type == "spikes":  # load the spikes sprites
                        sprite_group.add(StaticActor(
                            x, y, images[int(value)], int(TILE_SIZE/16)))
                    if type == "spawn":  # load the start sprites
                        sprite_group.add(Player(x, y, 1.5*int(TILE_SIZE/16)))
                    if type == "foliage":  # load the foliage sprites
                        sprite_group.add(StaticActor(
                            x, y, images[int(value)], int(TILE_SIZE/16)))
                    if type == "enemies":  # load the enemies sprites
                        sprite = Skeleton(x, y, randint(1,3), 2*int(TILE_SIZE/16))
                        sprite.rect.y -= sprite.rect.height/2
                        sprite_group.add(sprite)

        return sprite_group  # return the created sprite group

    def game_logic(self):
        # all game logic runs here
        self.spike_timer -= 1
        if self.spike_timer < 0:
            self.spike_timer = 0

        for player in self.player:
            for sprite in self.end_sprites:
                if player.rect.colliderect(sprite.rect):
                    if self.level_number < 3:  # level progression
                        player.next_level = True
                        victory_sound.play()
                    else:
                        # if all the enemies in level 3 are dead, you win
                        for boss in self.boss_sprites:
                            for enemy in boss.skeletons:
                                if enemy.alive is False:
                                    self.enemy_felled = True
                            if boss.alive is False:
                                self.boss_felled = True
                        if self.enemy_felled and self.boss_felled:
                            player.victory = True
                            victory_sound.play()

            # coin collection
            for sprite in self.coins_sprites:
                if player.rect.colliderect(sprite.rect):
                    player.score += 10  # increase stats and delete the sprite
                    sprite.kill()
                    pick_up.play()

            # health pick ups
            for sprite in self.health_sprites:
                if player.rect.colliderect(sprite.rect):
                    player.health += 30  # increase stats and delete the sprite
                    if player.health > player.max_health:
                        player.health = player.max_health
                    pick_up_2.play()
                    sprite.kill()

            for sprite in self.enemies_sprites:
                # take enemy health when in combat
                if sprite.alive and player.range_rect.colliderect(sprite.rect)\
                        and player.attack and player.take_target_hp:
                    sprite.health -= 40
                    slash.play()

            for sprite in self.boss_sprites:
                # take enemy health when in combat
                if sprite.alive and player.range_rect.colliderect(sprite.rect)\
                        and player.attack and player.take_target_hp:
                    sprite.health -= 40
                    slash.play()

            # spikes hurt player
            for sprite in self.spikes_sprites:
                if player.rect.colliderect(sprite.rect):
                    if self.spike_timer == 0:
                        player.health -= 10
                        self.spike_timer = 80

            # death if you fall off screen
            if player.rect.bottom > 720:
                player.alive = False
                player.health = 0

    def run(self, screen: pygame.Surface, font: pygame.font.Font):
        # show the backgrounds for each level
        if self.level_number < 3:
            screen.blit(self.bg_img1, (0, 0))
            screen.blit(self.bg_img2, (0, 0))

        # draw all the sprites
        self.bg_sprites.draw(screen)
        self.decor_sprites.draw(screen)
        self.end_sprites.draw(screen)
        self.health_sprites.draw(screen)
        self.floor_sprites .draw(screen)
        self.spikes_sprites.draw(screen)
        self.foliage_sprites.draw(screen)
        self.enemies_sprites.draw(screen)
        self.coins_sprites.draw(screen)
        self.boss_sprites.draw(screen)
        self.game_logic()

        # draw enemy healthbars
        for enemy in self.enemies_sprites:
            if enemy.alive:
                enemy.health_bar.draw(
                    enemy.animations['move'][0].get_width(), enemy.health, screen)
                enemy.health_bar.x = enemy.rect.left
                enemy.health_bar.y = enemy.rect.top

        for boss in self.boss_sprites:
            if boss.alive:
                boss.health_bar.draw(
                    boss.animations['move'][0].get_width(), boss.health, screen)
                boss.health_bar.x = boss.rect.left
                boss.health_bar.y = boss.rect.top

        # draw player and ui
        self.player.draw(screen)
        for p in self.player:
            draw_text(WIDTH*0.1, HEIGHT*0.1,
                      f"SCORE: {p.score}", font, screen, 'gold')
            p.health_bar.draw(
                p.animations['run'][0].get_width(), p.health, screen)

        # everything updates with respect to the player
        self.bg_sprites.update(self.player, self.level_number)
        self.constraints.update(self.player, self.level_number)
        self.decor_sprites.update(self.player, self.level_number)
        self.end_sprites.update(self.player, self.level_number)
        self.health_sprites.update(self.player, self.level_number)
        self.floor_sprites .update(self.player, self.level_number)
        self.spikes_sprites.update(self.player, self.level_number)
        self.foliage_sprites.update(self.player, self.level_number)
        self.coins_sprites.update(self.player, self.level_number)
        self.boss_sprites.update(
            screen, self.player, self.level_number, self.constraints)
        self.enemies_sprites.update(
            self.player, self.level_number, self.constraints)
        self.player.update(self.floor_sprites)
