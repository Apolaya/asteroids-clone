from pathlib import Path

import pygame

from . import globals, utilities
from .player import Player
from .asteroid import Asteroid

bg_path = Path("assets", "art", "background.png")


# This method runs the game and is called in the top-level main module
def run():
    pygame.init()
    screen = pygame.display.set_mode((globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT))
    background = pygame.image.load(bg_path)
    clock = pygame.time.Clock()
    running = True
    globals.DT = 0
    last_spawn = 0

    player = Player(
        pygame.math.Vector2((screen.get_width() / 2, screen.get_height() / 2))
    )
    globals.PLAYER_SPRITE.add(player)

    asteroid = Asteroid(utilities.spawn_location())
    globals.ASTEROID_SPRITES.add(asteroid)

    while running:
        current_tick = pygame.time.get_ticks()
        if current_tick - last_spawn >= globals.SPAWN_RATE:
            last_spawn = current_tick
            asteroid = Asteroid(utilities.spawn_location())
            globals.ASTEROID_SPRITES.add(asteroid)

        if len(globals.PLAYER_SPRITE) < 1:
            player = Player(
                pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            )
            globals.PLAYER_SPRITE.add(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        left_mouse, middle_mouse, right_mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_w]:
            player.move("UP")
        if keys[pygame.K_s]:
            player.move("DOWN")
        if keys[pygame.K_a]:
            player.move("LEFT")
        if keys[pygame.K_d]:
            player.move("RIGHT")
        if keys[pygame.K_SPACE] or left_mouse:
            player.shoot()

        globals.PLAYER_SPRITE.update()
        globals.ASTEROID_SPRITES.update()
        globals.PROJECTILE_SPRITES.update()
        screen.blit(background, (0, 0))

        if globals.LIVES < 1:
            print("Game over!")
            running = False
            break

        globals.PLAYER_SPRITE.draw(screen)
        globals.ASTEROID_SPRITES.draw(screen)
        globals.PROJECTILE_SPRITES.draw(screen)
        pygame.display.flip()

        print(globals.SCORE)

        # limits FPS and returns value for framerate-independent physics
        globals.DT = clock.tick(60) / 1000

    pygame.quit()
