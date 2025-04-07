import os
import pygame
from . import globals
from .player import Player

bg_path = os.path.join(os.path.dirname(__file__), '../assets/art/background.png')

# This method runs the game and is called in the top-level main module
def run():
    pygame.init()
    screen = pygame.display.set_mode((globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT))
    bg = pygame.image.load(bg_path)
    clock = pygame.time.Clock()
    running = True
    dt = 0
    all_sprites = pygame.sprite.Group()
    player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
    all_sprites.add(player)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update(dt)
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)

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
            player.shoot(all_sprites)

        pygame.display.flip()

        # limits FPS and returns value for framerate-independent physics
        dt = clock.tick(60) / 1000

    pygame.quit()
