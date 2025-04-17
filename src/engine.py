from pathlib import Path
import sys

import pygame

from . import globals
from .Player import Player
from .Asteroid import AsteroidManager
from .UI import UI, Modal, Button, Text


bg_path = Path("assets", "art", "background.png")
music_path = Path("assets", "sounds", "through_space.ogg")

"""This method runs the game and is called in the top-level main module."""
def run():
    """Initialize audio mixer and engine, set up display, start clock, and set starting state"""
    pygame.mixer.pre_init(44100, -16, 2, 64)
    pygame.mixer.init()
    if pygame.mixer.get_init():
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.2)

    pygame.init()

    screen = pygame.display.set_mode(
        (globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT))
    pygame.display.set_caption("Asteroid Survivors")
    background = pygame.image.load(bg_path)

    clock = globals.CLOCK
    state = "START"
    mouse = (-1, -1)
    respawn_timer = 3

    """Set up UI with reusable modal, text, and buttons"""
    ui = UI(screen)

    modal = Modal(
        (globals.WINDOW_WIDTH/2 - 200, globals.WINDOW_HEIGHT/2 - 200),
        (400, 400), (122, 122, 122)
    )

    header_text = Text(
        (0, 0), 32, (0, 0, 0), 
        "", "Courier", bold=True
    )
    header_text.rect.topleft = (modal.rect.w/2 - header_text.rect.w/2, 50)

    middle_text = Text(
        (0, 0), 32, (0, 0, 0),
        "Score: " + str(globals.SCORE),
        "Courier", bold=True
    )
    middle_text.rect.topleft = (modal.rect.w/2 - middle_text.rect.w/2, 85)

    middle_button = Button(
        (0,0), (200, 50),
        (0, 0, 0), ""
    )
    middle_button.rect.topleft = (
        modal.rect.w/2 - middle_button.rect.w/2, 
        modal.rect.h/2 - middle_button.rect.h/2
    )

    lower_button = Button(
        (0,0), (200, 50),
        (0, 0, 0), ""
    )
    lower_button.rect.topleft = (
        modal.rect.w/2 - lower_button.rect.w/2, 
        modal.rect.h/2 - lower_button.rect.h/2 + 75
    )

    scoreboard = Text(
        (10,10), 32, (255,255,255),
        "Score: " + str(globals.SCORE),
        "Courier", bold=True
    )
    ui.add(scoreboard)

    lives = Text(
        (250,10), 32, (255,255,255),
        "Lives: " + str(globals.LIVES),
        "Courier", bold=True
    )
    ui.add(lives)

    # Create Asteroid spawner and player
    spawner = AsteroidManager()
    spawner.start_game()

    player = Player(
        pygame.math.Vector2((screen.get_width() / 2, screen.get_height() / 2))
    )
    globals.PLAYER_SPRITE.add(player)

    pygame.mixer.music.play()

    # Enter game loop
    while True:

        # limits FPS and returns value for framerate-independent physics
        globals.DT = clock.tick(globals.FRAMERATE) / 1000

        # Set state based on input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state == "EXIT"
                pygame.quit()
                sys.exit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "PAUSED" if state == "RUNNING" else "RUNNING"

            if event.type == pygame.MOUSEBUTTONUP:
                mouse = event.pos

        # Run the correct logic based  on current state
        if state == "START":
            globals.LIVES = 3
            globals.SCORE = 0
            modal.clear()
            screen.blit(background, (0, 0))
            middle_button.set_text("Start")
            lower_button.set_text("Quit")
            header_text.set_text("Modern Asteroids")
            modal.add_all((header_text, middle_button, lower_button))
            ui.add(modal)
            ui.draw()
            pygame.display.flip()
            state = "WAITING"
            continue

        # On pause, stop the simulation and display the pause modal
        if state == "PAUSED":
            modal.clear()
            screen.blit(background, (0, 0))
            middle_button.set_text("Resume")
            lower_button.set_text("Quit")
            header_text.set_text("Paused")
            modal.add_all((header_text, middle_button, lower_button))
            ui.add(modal)
            ui.draw()
            pygame.display.flip()
            state = "WAITING"
            continue

        # On running out of lives, display the game over modal
        if state == "GAMEOVER":
            modal.clear()
            screen.blit(background, (0, 0))
            middle_button.set_text("Retry")
            lower_button.set_text("Quit")
            header_text.set_text("Game over!")
            middle_text.set_text("Score: " + str(globals.SCORE))
            modal.add_all((header_text, middle_text, middle_button, lower_button))
            ui.add(modal)
            ui.draw()
            pygame.display.flip()
            state = "WAITING"
            continue
            
        #Transition to waiting state while modal is presented
        if state == "WAITING":
            clicked = modal.check_click(mouse)
            match clicked:
                case 'Retry':
                    mouse = (-1, -1)
                    state = 'START'
                case 'Start' | 'Resume':
                    mouse = (-1, -1)
                    state = 'RUNNING'
                case 'Quit':
                    pygame.quit()
                    sys.exit()
                    return
            continue

        # Standard gameplay state to run simulation
        if state == "RUNNING":
            if(modal in ui.children):
              ui.remove(modal)
            # If player is destroyed, respawn and reset wave
            if len(globals.PLAYER_SPRITE) < 1:
                respawn_timer -= globals.DT
                if respawn_timer <= 0:
                    respawn_timer = 3
                    spawner.reset_game()
                    player = Player(
                        pygame.Vector2(screen.get_width() / 2,
                                       screen.get_height() / 2)
                    )
                    globals.PLAYER_SPRITE.add(player)

            # Respond to continuous input from keys and mouse
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

            # Update all sprites and the UI
            spawner.update()
            globals.PLAYER_SPRITE.update()
            globals.ASTEROID_SPRITES.update()
            globals.PROJECTILE_SPRITES.update()
            scoreboard.set_text("Score: " + str(globals.SCORE))
            lives.set_text("Lives: " + str(globals.LIVES))
            screen.blit(background, (0, 0))

            # Handle collisions and increment score
            points, resources = spawner.handle_collision()
            globals.SCORE += points

            # Check for game over
            if globals.LIVES < 1:
                state = "GAMEOVER"

            # Draw all sprites to display
            globals.PLAYER_SPRITE.draw(screen)
            globals.ASTEROID_SPRITES.draw(screen)
            globals.PROJECTILE_SPRITES.draw(screen)
            ui.draw()
            pygame.display.flip()
